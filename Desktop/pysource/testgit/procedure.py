import os

fileName = "LJ"
fileName2 = "LJ.argus"
fileName3 = "LJ.csv"
fileName4 = "LJ_clean.csv"
loc_fileName4 = "~/Desktop/data/"
fileName5 = "LJ_prob.csv"
data_cleaner_name = "data_cleaner"

#os.system("tshark -c 500 -w "+fileName)
os.system("argus -r "+fileName+" -w "+fileName2)
os.system("ra -n -c, -r "+
	fileName2+
	" -s saddr"+
	" daddr proto sport dport state stos dtos swin dwin"+
	" shops dhops stime ltime sttl dttl tcprtt synack ackdat"+
	" spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts"+
	" bytes appbytes rate srate drate label > "+
	fileName3)

os.system("javac "+data_cleaner_name+".java")
os.system("java  "+data_cleaner_name+
	" "+
	fileName3+
	" "+
	fileName4)
#os.system("source ~/tensorflow/bin/activate")
os.system("python testparsing.py "+loc_fileName4+fileName4+" "+fileName5)
print("celebration granted")
