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
CONTINUOUS_COLUMNS = ["State","SrcPkts","Sport","Dport","SrcWin","sTtl","Rate","SrcBytes","TotBytes","TotPkts","StartTime","SrcRate","SrcAddr","sHops","dHops","sTtl","dTtl","sTos"]



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
 
  return feature_cols, df["SrcAddr"]



def test_predict_fn():
  df_test = pd.read_csv(str(sys.argv[1]),names=COLUMNS, skiprows=1)
  
  return input_fn(df_test)



def main():
    Proto = tf.contrib.layers.sparse_column_with_keys(
      column_name="Proto", keys=["tcp","udp","icmp"])
    State = tf.contrib.layers.sparse_column_with_keys(
      column_name="State", keys=["RST","FIN","CON","INT","URP","URN","ACC"])
   

    #StartTime = tf.contrib.layers.real_valued_column("StartTime")
    SrcPkts = tf.contrib.layers.real_valued_column("SrcPkts")
    #SrcAddr = tf.contrib.layers.real_valued_column("SrcAddr")
    SrcBytes = tf.contrib.layers.real_valued_column("SrcBytes")
    TotPkts = tf.contrib.layers.real_valued_column("TotPkts")

    sHops = tf.contrib.layers.real_valued_column("sHops")
    sTtl = tf.contrib.layers.real_valued_column("sTtl")
    TotBytes = tf.contrib.layers.real_valued_column("TotBytes")
    SrcBytes = tf.contrib.layers.real_valued_column("SrcBytes")
    Sport = tf.contrib.layers.real_valued_column("Sport")
    Dport = tf.contrib.layers.real_valued_column("Dport")
    SrcWin= tf.contrib.layers.real_valued_column("SrcWin")


    
    with tf.Session() as sess:
      model_dir = "model_2"#tempfile.mkdtemp()               #5      19      21       26      27
      m = tf.contrib.learn.LinearClassifier(feature_columns=[State,SrcPkts,SrcBytes,TotPkts,TotBytes],
      model_dir=model_dir)
      

      tf.global_variables_initializer()

      
      x_predict, df_SrcAddr = test_predict_fn()
      pred_proba = m.predict_proba(input_fn=lambda: test_predict_fn())
     

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
            #alert something!!!
            f.write(str(sys.argv[1]) + ","
              + str(result['SrcAddr'].loc[i]) + ","
              + str(result['botnet'].loc[i]) + "\n")   



    print("done")
    

    
main()