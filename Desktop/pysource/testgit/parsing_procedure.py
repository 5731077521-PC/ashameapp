import pandas as pd
import numpy as np
import tempfile
import os,sys
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
CONTINUOUS_COLUMNS = ["SrcBytes","SrcPkts","TotPkts","TotBytes","Rate","StartTime","SrcRate","SrcAddr","sHops","dHops","sTtl","dTtl","sTos"]

train_file = '~/Desktop/pysource/data/cap44aa_clean.csv'
test_file = '~/Desktop/pysource/data/cap43aa_clean.csv'
LJ = '~/Desktop/data/LJ_clean.py'

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
  
    return struct.unpack("!L", packedIP)[0]
  except Exception as e:
    return 0
      
  

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
  #label = tf.constant(df[LABEL_COLUMN].values)
  # Returns the feature columns and the label.
  return feature_cols, df["SrcAddr"]

def train_input_fn():
  df_train =  pd.read_csv(train_file,names=COLUMNS, skiprows=1)
  df_train[LABEL_COLUMN] = (df_train["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  df_train["SrcAddr"] = ((df_train["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  #df_train["StartTime"] = ((df_train["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_train)

def eval_input_fn():
  df_test = pd.read_csv(test_file,names=COLUMNS, skiprows=1)
  df_test[LABEL_COLUMN] = (df_test["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  df_test["SrcAddr"] = ((df_test["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  #df_test["StartTime"] = ((df_test["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_test)

def test_predict_fn():
  df_test = pd.read_csv(str(sys.argv[1]),names=COLUMNS, skiprows=1)
  #df_test[LABEL_COLUMN] = (df_test["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  #df_test["SrcAddr"] = ((df_test["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  #df_test["StartTime"] = ((df_test["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_test)


def confusion(m,threshold,df_eval):
  pred_proba = m.predict_proba(input_fn=lambda: test_predict_fn())
  pred_df = pd.DataFrame(list(pred_proba), columns=['normal','botnet'])
  pred_df['botnet'] = (pred_df["botnet"].apply(lambda x: x>threshold)).astype(int)
  pred_df_botnet = pred_df['botnet']
  eval_df_botnet = df_eval[LABEL_COLUMN]


  tp, tn, fp, fn = 0,0,0,0
  for idx, item in enumerate(eval_df_botnet):

    if eval_df_botnet[idx] == 1:
      if(pred_df_botnet[idx] == 0):
        fn += 1
      if(pred_df_botnet[idx] == 1):
        tp += 1



    if eval_df_botnet[idx] == 0:
      if(pred_df_botnet[idx] == 0):
        tn += 1
      if(pred_df_botnet[idx] == 1):
        fp += 1
  

  total = tp+tn+fp+fn
  correct_result = tp+tn

  
  return correct_result/total, fn


def main():
    print(111)
    
    Proto = tf.contrib.layers.sparse_column_with_keys(
      column_name="Proto", keys=["tcp","udp","icmp"])
    State = tf.contrib.layers.sparse_column_with_keys(
      column_name="State", keys=["RST","FIN","CON","INT","URP","URN","ACC"])
   

    #StartTime = tf.contrib.layers.real_valued_column("StartTime")
    SrcPkts = tf.contrib.layers.real_valued_column("SrcPkts")
    #SrcAddr = tf.contrib.layers.real_valued_column("SrcAddr")
    SrcBytes = tf.contrib.layers.real_valued_column("SrcBytes")
    TotPkts = tf.contrib.layers.real_valued_column("TotPkts")
    TotBytes = tf.contrib.layers.real_valued_column("TotBytes")
    #dTtl = tf.contrib.layers.real_valued_column("dTtl")
    sTos = tf.contrib.layers.real_valued_column("sTos")
    Rate = tf.contrib.layers.real_valued_column("Rate")



    print(888)

    
    with tf.Session() as sess:
      model_dir = "model_2"#tempfile.mkdtemp()               #5      19      21       26      27
      m = tf.contrib.learn.LinearClassifier(feature_columns=[State,SrcPkts,SrcBytes,TotPkts,TotBytes],
      model_dir=model_dir)

      #init_op = tf.global_variables_initializer()
      #sess = tf.Session()
      #sess.run(init_op)

      #m.fit(input_fn=lambda: train_input_fn(), steps=200)
      tf.global_variables_initializer()
    
      
    
      
    

      

      
      x_predict, df_SrcAddr = test_predict_fn()
      pred_proba = m.predict_proba(input_fn=lambda: test_predict_fn())
     


      #x_train, df_SrcAddr = test_predict_fn()
      writes = csv.writer(open(str(sys.argv[2]), 'w', newline=''), delimiter=',', quoting=csv.QUOTE_ALL)
      writes.writerows(pred_proba)

      pred_filter = m.predict_proba(input_fn=lambda: test_predict_fn())
      pred_df = pd.DataFrame(data=list(pred_filter), columns=['normal','botnet'])
      result = pd.concat([df_SrcAddr,pred_df['normal'],pred_df['botnet']], axis=1, join='inner')
      #result.to_csv('/home/netklause/Desktop/data/sandbox/prob_dump/result-2.csv')
      notify = pd.DataFrame(columns=['SrcAddr','val','line'])
      threshold_filter = 1e-10

      with open("/home/netklause/Desktop/data/sandbox/prob_dump/filtered.csv", 'a') as f:
        for i in range(len(result.index)) :
          if(result['botnet'].loc[i]>threshold_filter):
            f.write(str(sys.argv[1]) + ","
              + str(result['SrcAddr'].loc[i]) + ","
              + str(result['botnet'].loc[i]) + "\n")   



            
          
      """
      pred_df = pd.DataFrame(list(pred_proba), columns=['normal','botnet'])
      pred_df['botnet'] = (pred_df["botnet"].apply(lambda x: x>0.5)).astype(int)
      #dfx.to_csv('writtenbydfx.csv')
      pred_df_botnet = pred_df['botnet']
      eval_df_botnet = df_eval[LABEL_COLUMN] 
  
      #input_list = list(np.arange(0.1,0.5,0.1)) 
    
      input_list = [1e-30] 

      for threshold in input_list:
         accuracy, fn = confusion(m,threshold, df_eval)
         print("accuracy of ",threshold," : ",accuracy," ,  "
          "fn : ",fn)  """
      
      

   
    
    

    print("done")
    

    
    
  

    
main()