import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# This program require these software : argus , ra (read argus)
# This program must be deployed in this environment condition : python 3.6, tensorflow 1.x
# This program need these files residing in the same directory : data_cleaner.java , tensorflow_model.py
# This program requires folders for dump of capture (dumpFolder), dump of output (prob_dumpDir)

currentDir = "/home/netklause/Desktop/data/sandbox/" #directory of this file
data_cleaner_name = "data_cleaner"
dumpFolder = "dump_3/" 								 #directory of generated file
dumpDir = currentDir+dumpFolder
probFolder = "prob_dump/"
#prob_dumpDir = "~/Desktop/data/sandbox/prob_dump/"	 #directory of output probabilty file
prob_dumpDir = currentDir+probFolder

def procedure(capture):

	argusFile = capture + '.argus'
	rawInputFile = capture + '_raw.csv'
	cleanInputFile = capture + '_clean.csv'
	generatedProb = capture + "_prob.csv"

	
	os.system("argus -r " + dumpDir+capture + " -w " + dumpDir+argusFile)
	time.sleep(2)

	os.system("ra -n -c, -r "+
		dumpDir+argusFile+
		" -s saddr"+
		" daddr proto sport dport state stos dtos swin dwin"+
		" shops dhops stime ltime sttl dttl tcprtt synack ackdat"+
		" spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts"+
		" bytes appbytes rate srate drate > "+
		dumpDir+rawInputFile)

	os.system("java  "+data_cleaner_name+
		" "+
		dumpDir+rawInputFile+
		" "+
		dumpDir+cleanInputFile)
	time.sleep(1)
	os.system("python tensorflow_model.py "+dumpDir+cleanInputFile+" "+prob_dumpDir+generatedProb) 
	



class NewCreatedFileHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        createdFileName = str(event.src_path)[-28:] #substring for the name of pcap file from backward : capture_xxxxx_timestamp...
        if(createdFileName[:len('capture')] == 'capture'): #capture
        	print("Got event for file " , createdFileName)
        	time.sleep(2)
        	procedure(createdFileName)
        else:
        	print("Got event for file " , str(event.src_path)[44:]) #42 #cut dir string
      		




def main(): 
	observer = Observer()
	event_handler = NewCreatedFileHandler() # create event handler
	# set observer to use created handler in directory
	observer.schedule(event_handler, path=dumpDir)
	observer.start()

	os.system("tshark -n -i any -a filesize:5 -b files:5000 -w "+dumpDir+"capture"+" -F libpcap")

	# sleep until keyboard interrupt, then stop + rejoin the observer
	try:
		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		observer.stop()
    	

	observer.join()


main()
