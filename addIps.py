from DataHandler import DataHandler
import sys

handler = DataHandler()

for line in sys.stdin:

	line = line.replace("\n","")
	line = line.replace("\r","")
	line = line.replace(" ","")
	
	if(line != ""):
		print line
		handler.addIp(line,443)
