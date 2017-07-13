import pandas as pd
import numpy as np
import tempfile
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import socket, struct
import time
from calendar import timegm
import sys, csv

COLUMNS = ["SrcAddr","DstAddr","Proto","Sport","Dport","State","sTos","dTos","SrcWin","DstWin"
          ,"sHops","dHops","StartTime","LastTime","sTtl","dTtl","TcpRtt","SynAck","AckDat","SrcPkts"
          ,"DstPkts","SrcBytes","DstBytes","SAppBytes","DAppbytes","Dur","TotPkts","TotBytes"
          ,"TotAppByte","Rate","SrcRate","DstRate","Tag"]
LABEL_COLUMN = "label"
CATEGORICAL_COLUMNS = ["Proto","State","Tag"]
CONTINUOUS_COLUMNS = ["StartTime","SrcRate","SrcAddr","sHops","dHops","sTtl","dTtl"]
IP_COLUMNS = ["NewAddr"]

train_file = '~/Desktop/pysource/rawdata2-1.csv'
test_file = '~/Desktop/pysource/rawdata2-2.csv'

def stamp2epoch(timestamp):
  utc_time = time.strptime(timestamp, "%m-%d-%Y %H:%M:%S")
  epoch_time = timegm(utc_time)
  return epoch_time

def ip2long(ip):
  """
  Convert an IP string to long
  """
  try: 
    packedIP = socket.inet_aton(ip)
    raise Exception('never mind')
    return struct.unpack("!L", packedIP)[0]
  except Exception as e:
    print('we will not catch e')
      
  return '0'

def input_fn(df):

  # Creates a dictionary mapping from each continuous feature column name (k) to
  # the values of that column stored in a constant Tensor.
  continuous_cols = {k: tf.constant(df[k].values)
                     for k in CONTINUOUS_COLUMNS}
  # Creates a dictionary mapping from each categorical feature column name (k)
  # to the values of that column stored in a tf.SparseTensor.
  categorical_cols = {k: tf.SparseTensor(
      indices=[[i, 0] for i in range(df[k].size)],
      values=df[k].values,
      dense_shape=[df[k].size, 1])
                      for k in CATEGORICAL_COLUMNS}

  
  # Merges the two dictionaries into one.
  #feature_cols = dict(continuous_cols.items() + categorical_cols.items())

  feature_cols = dict(continuous_cols)
  feature_cols.update(categorical_cols)
  #feature_cols.update(dict(ip_cols))
  # Converts the label column into a constant Tensor.
  label = tf.constant(df[LABEL_COLUMN].values)
  # Returns the feature columns and the label.
  return feature_cols, label

def train_input_fn():
  df_train =  pd.read_csv(train_file,names=COLUMNS, skiprows=1)
  df_train[LABEL_COLUMN] = (df_train["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  #df_train["SrcAddr"] = ((df_train["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  #df_train["StartTime"] = ((df_train["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_train)

def eval_input_fn():
  df_test = pd.read_csv(test_file,names=COLUMNS, skiprows=1)
  df_test[LABEL_COLUMN] = (df_test["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  #df_test["SrcAddr"] = ((df_test["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  #df_test["StartTime"] = ((df_test["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_test)

def test_predict_fn():
  df_test = pd.read_csv(test_file,names=COLUMNS, skiprows=1)
  df_test[LABEL_COLUMN] = (df_test["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  #df_test["SrcAddr"] = ((df_test["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  #df_test["StartTime"] = ((df_test["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_test)





def main():
    print(111)

    Proto = tf.contrib.layers.sparse_column_with_keys(
      column_name="Proto", keys=["tcp","udp","icmp"])
    State = tf.contrib.layers.sparse_column_with_keys(
      column_name="State", keys=["RST","FIN","CON","INT","URP","URN","ACC"])
    Tag = tf.contrib.layers.sparse_column_with_keys(
      column_name="Tag", keys=["xxx","Botnet"])

    StartTime = tf.contrib.layers.real_valued_column("StartTime")
    SrcRate = tf.contrib.layers.real_valued_column("SrcRate")
    SrcAddr = tf.contrib.layers.real_valued_column("SrcAddr")
    sHops = tf.contrib.layers.real_valued_column("sHops")
    dHops = tf.contrib.layers.real_valued_column("dHops")
    sTtl = tf.contrib.layers.real_valued_column("sTtl")
    dTtl = tf.contrib.layers.real_valued_column("dTtl")

    print(333)

    model_dir = tempfile.mkdtemp()
    m = tf.contrib.learn.LinearClassifier(feature_columns=[SrcRate,sHops,dHops,sTtl],
    model_dir=model_dir)

    #init_op = tf.global_variables_initializer()
    #sess = tf.Session()
    #sess.run(init_op)

    m.fit(input_fn=lambda: train_input_fn(), steps=200)
    
    
    results = m.evaluate(input_fn=lambda: eval_input_fn(), steps=1)
    for key in sorted(results):
      print("%s: %s" % (key, results[key]))

    df_eval = pd.read_csv(test_file,names=COLUMNS, skiprows=1)
    df_eval[LABEL_COLUMN] = (df_eval["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
    df_SrcAddr = df_eval['SrcAddr']

    pred_proba = m.predict_proba(input_fn=lambda: test_predict_fn())

    
    #writes = csv.writer(open('testprob_resultxxx.csv', 'w', newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
    #writes.writerows(pred_proba)
	
    pred_df = pd.DataFrame(list(pred_proba), columns=['normal','botnet'])
    pred_df['botnet'] = (pred_df["botnet"].apply(lambda x: x>0.5)).astype(int)
    #dfx.to_csv('writtenbydfx.csv')
    pred_df_botnet = pred_df['botnet']
    eval_df_botnet = df_eval[LABEL_COLUMN]

    tp, tn, fp, fn = 0,0,0,0

   




    
    
    for idx, item in enumerate(eval_df_botnet):
    	if eval_df_botnet[idx] == 0:
    		if(pred_df_botnet[idx] == 0): 
    			tn += 1
    		if(pred_df_botnet[idx] == 1): 
    			fp += 1

    	if eval_df_botnet[idx] == 1:
    		if(pred_df_botnet[idx] == 0): 
    			fn += 1
    			print(str(df_SrcAddr[idx]))
    		if(pred_df_botnet[idx] == 1):
    			tp += 1

    print("done")
    

  	
    
 	

    
main()