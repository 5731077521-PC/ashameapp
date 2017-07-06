import pandas as pd
import numpy as np
import tempfile
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import socket, struct
import time
from calendar import timegm
#notify change
#notify change
COLUMNS = ["SrcAddr","DstAddr","Proto","Sport","Dport","State","sTos","dTos","SrcWin","DstWin"
          ,"sHops","dHops","StartTime","LastTime","sTtl","dTtl","TcpRtt","SynAck","AckDat","SrcPkts"
          ,"DstPkts","SrcBytes","DstBytes","SAppBytes","DAppbytes","Dur","TotPkts","TotBytes"
          ,"TotAppByte","Rate","SrcRate","DstRate","Tag"]
LABEL_COLUMN = "label"
CATEGORICAL_COLUMNS = ["Proto","State","Tag"]
CONTINUOUS_COLUMNS = ["StartTime","SrcRate","SrcAddr","sHops","dHops","sTtl","dTtl"]
IP_COLUMNS = ["NewAddr"]

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

  ip_cols = {tf.constant(df["SrcAddr"].values)}
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
  train_file = '~/Desktop/pysource/eval4.csv'
  df_train =  pd.read_csv(train_file,names=COLUMNS, skiprows=1)
  df_train[LABEL_COLUMN] = (df_train["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  df_train["SrcAddr"] = ((df_train["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  df_train["StartTime"] = ((df_train["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_train)

def eval_input_fn():
  test_file = '~/Desktop/pysource/eval5.csv'
  df_test = pd.read_csv(test_file,names=COLUMNS, skiprows=1)
  df_test[LABEL_COLUMN] = (df_test["Tag"].apply(lambda x: "Botnet" in x)).astype(int)
  df_test["SrcAddr"] = ((df_test["SrcAddr"].astype('str')).apply(ip2long)).astype(int)
  df_test["StartTime"] = ((df_test["StartTime"].astype('str')).apply(stamp2epoch)).astype(int)
  
  return input_fn(df_test)



def main():
    print(111)

    Proto = tf.contrib.layers.sparse_column_with_keys(
      column_name="Proto", keys=["tcp","udp","icmp"])
    State = tf.contrib.layers.sparse_column_with_keys(
      column_name="State", keys=["RST","FIN","CON","INT","URP","URN"])
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
    m = tf.contrib.learn.LinearClassifier(feature_columns=[SrcAddr,SrcRate,StartTime,sHops,dHops,sTtl,dTtl],
    model_dir=model_dir)

  

    m.fit(input_fn=lambda: train_input_fn(), steps=200)
    
    
    results = m.evaluate(input_fn=lambda: eval_input_fn(), steps=1)
    for key in sorted(results):
      print("%s: %s" % (key, results[key]))
    
    print("done")
    
  #df_pre_eval[LABEL_COLUMN] = (df_pre_eval["Tag"].apply(lambda x: "Botnet" in x)).astype(int)

"""
  Proto = tf.contrib.layers.sparse_column_with_keys(
  column_name="Proto", keys=["tcp", "udp","icmp"])
  State = tf.contrib.layers.sparse_column_with_keys(
  column_name="State", keys=["RST", "FIN","CON","INT","URP","URN"])
"""
  
  
  #SrcAddr = tf.contrib.layers.sparse_column_with_hash_bucket("SrcAddr", hash_bucket_size=1000)
  
"""
  stAddr = tf.contrib.layers.sparse_column_with_hash_bucket("DstAddr", hash_bucket_size=1000)
  Sport = tf.contrib.layers.sparse_column_with_hash_bucket("Sport", hash_bucket_size=1000)
  Dport = tf.contrib.layers.sparse_column_with_hash_bucket("Dport", hash_bucket_size=1000)
  sTos = tf.contrib.layers.sparse_column_with_hash_bucket("sTos", hash_bucket_size=1000)
  dTos = tf.contrib.layers.sparse_column_with_hash_bucket("dTos", hash_bucket_size=1000)
  SrcWin = tf.contrib.layers.sparse_column_with_hash_bucket("SrcWin", hash_bucket_size=1000)
  DstWin = tf.contrib.layers.sparse_column_with_hash_bucket("DstWin", hash_bucket_size=1000)
  StartTime = tf.contrib.layers.sparse_column_with_hash_bucket("StartTime", hash_bucket_size=1000)
  LastTime = tf.contrib.layers.sparse_column_with_hash_bucket("LastTime", hash_bucket_size=1000)
  Tag = tf.contrib.layers.sparse_column_with_hash_bucket("Tag", hash_bucket_size=1000)

  SrcAddr_x_DstAddr_x_Sport_x_Dport = tf.contrib.layers.crossed_column([SrcAddr, DstAddr, Sport, Dport], hash_bucket_size=int(1e6))
"""
  
    
"""
  TcpRtt = tf.contrib.layers.real_valued_column("TcpRtt")
  SynAck = tf.contrib.layers.real_valued_column("SynAck")
  AckDat = tf.contrib.layers.real_valued_column("AckDat")
  SrcPkts = tf.contrib.layers.real_valued_column("SrcPkts")
  DstPkts = tf.contrib.layers.real_valued_column("DstPkts")
  SrcBytes = tf.contrib.layers.real_valued_column("SrcBytes")
  DstBytes = tf.contrib.layers.real_valued_column("DstBytes")
  SAppBytes = tf.contrib.layers.real_valued_column("SAppBytes")
  DAppBytes = tf.contrib.layers.real_valued_column("DAppBytes")
  Dur = tf.contrib.layers.real_valued_column("Dur")
"""
"""

  sTtl_bucket = tf.contrib.layers.bucketized_column(sTtl, boundaries=[40,80,120,160,200,240,280])
  dTtl_bucket = tf.contrib.layers.bucketized_column(dTtl, boundaries=[40,80,120,160,200,240])
  #TcpRtt_bucket = tf.contrib.layers.bucketized_column(TcpRtt, boundaries=[1])
  #SynAck_bucket = tf.contrib.layers.bucketized_column(SynAck, boundaries=[40,80,120,160,200,240])
  #AckDat_bucket = tf.contrib.layers.bucketized_column(AckDat, boundaries=[40,80,120,160,200,240])
  SrcPkts_bucket = tf.contrib.layers.bucketized_column(SrcPkts, boundaries=[2,4,6,8,10,12,14,16,18,20])
  DstPkts_bucket = tf.contrib.layers.bucketized_column(DstPkts, boundaries=[2,4,6,8,10,12,14,16,18,20])
  SrcBytes_bucket =tf.contrib.layers.bucketized_column(SrcBytes, boundaries=[100,200,300,400,500,600,700,800,900,1000])
  DstBytes_bucket = tf.contrib.layers.bucketized_column(DstBytes, boundaries=[100,200,300,400,500,600,700,800,900,1000])
  SAppBytes_bucket = tf.contrib.layers.bucketized_column(SAppBytes, boundaries=[40,80,120,160,200,240])
  DAppBytes_bucket = tf.contrib.layers.bucketized_column(DAppBytes, boundaries=[40,80,120,160,200,240])

    print(333)

    model_dir = tempfile.mkdtemp()
    m = tf.contrib.learn.LinearClassifier(feature_columns=[sHops,dHops,sTtl,dTtl],
    model_dir=model_dir)

  

    m.fit(input_fn=lambda: train_input_fn(), steps=200)

    results = m.evaluate(input_fn= eval_input_fn, steps=1)
    for key in sorted(results):
      print("%s: %s" % (key, results[key]))

  results = m.evaluate(input_fn=eval_input_fn, steps=1)
  print(444)
  for key in sorted(results):
    print("%s: %s" % (key, results[key]))
"""
    


main()
