from CurlHandler import CurlHandler
from DataHandler import DataHandler

import sys

while True:

	try:
		dataHandler = DataHandler()
		ip = dataHandler.getRandomHTTPS()

		if ip == "":
			print "Could not find any ips that need processing"
			for x in range(0,1000):
				dataHandler.addRandomIp(443)
			sys.exit()

		print "Processing "+ip

		curlHandler = CurlHandler()
	
		response = curlHandler.getResponse(ip)

		dataHandler.setBanner(ip, 443, response)
	except:
		print "Having issues, skipping address"
