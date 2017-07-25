import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

dumpFolder = "dump_3"+"/"
dumpDir = "/home/netklause/Desktop/data/sandbox/"+dumpFolder


def procedure(capture):

	argusFile = capture + '.argus'
	rawInputFile = capture + '_raw.csv'
	cleanInputFile = capture + '_clean.csv'
	cleanInputDir = "~/Desktop/data/sandbox/"
	generatedProb = capture + "_prob.csv"
	data_cleaner_name = "data_cleaner_beta"
	#dumpDir = "~/Desktop/data/sandbox/dump_2/"
	prob_dumpDir = "~/Desktop/data/sandbox/prob_dump/"

	
	os.system("argus -r " + dumpDir+capture + " -w " + dumpDir+argusFile)
	time.sleep(2)
	#time.sleep(1)
	#os.system("ra -r "+dumpDir+argusFile)
	os.system("ra -n -c, -r "+
		dumpDir+argusFile+
		" -s saddr"+
		" daddr proto sport dport state stos dtos swin dwin"+
		" shops dhops stime ltime sttl dttl tcprtt synack ackdat"+
		" spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts"+
		" bytes appbytes rate srate drate > "+
		dumpDir+rawInputFile)

	#os.system("javac "+data_cleaner_name+".java")
	os.system("java  "+data_cleaner_name+
		" "+
		dumpDir+rawInputFile+
		" "+
		dumpDir+cleanInputFile)
	time.sleep(1)
	os.system("python parsing_procedure.py "+dumpDir+cleanInputFile+" "+prob_dumpDir+generatedProb) 
	



class NewCreatedFileHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        createdFileName = str(event.src_path)[-28:]
        if(createdFileName[:7] == 'capture'):
        	print("Got event for file " , createdFileName)
        	time.sleep(2)
        	procedure(createdFileName)
        else:
        	print("Got event for file " , str(event.src_path)[44:]) #42
      		




def main(): 
	observer = Observer()
	event_handler = NewCreatedFileHandler() # create event handler
	# set observer to use created handler in directory
	observer.schedule(event_handler, path=dumpDir)
	observer.start()

	os.system("tshark -n -i any -a filesize:5 -b files:500 -w "+dumpDir+"capture")

	# sleep until keyboard interrupt, then stop + rejoin the observer
	try:
		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		observer.stop()
    	

	observer.join()


main()
