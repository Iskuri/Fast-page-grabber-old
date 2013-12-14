import adodb
from random import randint

class DataHandler:

	conn = None

	def __init__(self):
	
		self.conn = adodb.NewADOConnection('mysql')
		self.conn.Connect('192.168.1.95','root','disappointed1','banner_quickscan')
		

	def getRow(self, query):

		cursor = self.conn.Execute(query)

		if cursor.EOF:
			return {}

		return cursor.GetRowAssoc(0)

	def addRandomIp(self, port):
		randomIp = str(randint(0, 255))+"."+str(randint(0, 255))+"."+str(randint(0, 255))+"."+str(randint(0, 255))
		print randomIp
		self.addIp(randomIp,port)

	def addIp(self, ip_address, port):

		if not self.getRow("SELECT * FROM ip_queue WHERE ip_address = '"+ip_address+"' AND port = "+str(port)):
			if not self.getRow("SELECT * FROM processed_ips i JOIN banners b ON b.ip_address_id = i.id WHERE ip_address = '"+ip_address+"' AND port = "+str(port)):
			#if not self.getRow("SELECT * FROM processed_ips i WHERE ip_address = '"+ip_address+"'"):
				#self.conn.Execute("INSERT INTO ip_queue(ip_address,port) VALUES ('"+ip_address+"', "+str(port)+");")
				self.conn.Execute("INSERT DELAYED INTO ip_queue(ip_address,port) VALUES ('"+ip_address+"', "+str(port)+");")

	def getProcessedIpId(self, ip_address):
		row = self.getRow("SELECT * FROM processed_ips WHERE ip_address = '"+ip_address+"'")
		
		if not row:
			self.conn.Execute("INSERT INTO processed_ips(ip_address) VALUES ('"+ip_address+"')")
			row = self.getRow("SELECT * FROM processed_ips WHERE ip_address = '"+ip_address+"'")
		return row['id']

	def getRandomHTTPS(self):
		#row = self.getRow("SELECT id, ip_address FROM ip_queue WHERE in_use IS FALSE AND port = 443 ORDER BY id DESC LIMIT 1")
		#row = self.getRow("SELECT id, ip_address FROM ip_queue WHERE in_use IS FALSE AND port = 443 AND ip_address LIKE '195.50%' ORDER BY id DESC LIMIT 1")
		row = self.getRow("SELECT id, ip_address FROM ip_queue WHERE in_use IS FALSE AND port = 443 ORDER BY RAND() LIMIT 1")
		if row:
			self.conn.Execute("UPDATE ip_queue SET in_use = TRUE WHERE id = "+str(row['id']))
		else:
			return ""

		return row['ip_address']
	
	def setBanner(self,ip_address,port,banner):

		ipAddressId = self.getProcessedIpId(ip_address)
		self.conn.Execute("INSERT INTO banners (ip_address_id, port, banner) VALUES ("+str(ipAddressId)+", "+str(port)+",'"+banner+"')")
		self.conn.Execute("DELETE FROM ip_queue WHERE ip_address = '"+ip_address+"' AND port = "+str(port))
