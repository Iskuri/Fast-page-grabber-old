import adodb

class DataHandler:

	conn = None

	def __init__(self):
	
		self.conn = adodb.NewADOConnection('mysql')
		self.conn.Connect('192.168.1.95','root','disappointed1','telnet_banners')
		
	def getRandom(self):

		#self.conn.BeginTrans()

		row = self.getRow("SELECT * FROM banners WHERE in_use IS FALSE AND dead_ip IS FALSE AND banner IS NULL ORDER BY RAND() LIMIT 1");

		if not row:
			return ''

		self.conn.Execute("UPDATE banners SET in_use = TRUE WHERE id = %d" % row['id'])

		#self.conn.CommitTrans()
		return row['ip_address']

	def getRandomHTTPS(self):

		#self.conn.BeginTrans()

                row = self.getRow("SELECT * FROM banners WHERE in_use IS FALSE AND dead_ip IS FALSE AND https_page_content IS NULL ORDER BY RAND() LIMIT 1");

                if not row:
                        return ''

                self.conn.Execute("UPDATE banners SET in_use = TRUE WHERE id = %d" % row['id'])

                #self.conn.CommitTrans()
                return row['ip_address']


	def getRow(self, query):

		cursor = self.conn.Execute(query)

		if cursor.EOF:
			return {}

		return cursor.GetRowAssoc(0)
	
	def addIp(self, ip_address):

		if not self.getRow("SELECT * FROM banners WHERE ip_address = '"+ip_address+"'"):
			self.conn.Execute("INSERT INTO banners(ip_address) VALUES ('"+ip_address+"');")

	def setBanner(self, ip_address, banner):

		if banner == '':
			self.conn.Execute("UPDATE banners SET dead_ip = TRUE, in_use = FALSE  WHERE ip_address = '"+ip_address+"'")			
		else:
			self.conn.Execute("UPDATE banners SET banner = '"+banner+"', in_use = FALSE WHERE ip_address = '"+ip_address+"'")

	def setHTTPSPage(self, ip_address, response):

	        if response == '':
                        self.conn.Execute("UPDATE banners SET dead_ip = TRUE, in_use = FALSE  WHERE ip_address = '"+ip_address+"'")
                else:
                        self.conn.Execute("UPDATE banners SET https_page_content = %s, in_use = FALSE WHERE ip_address = '"+ip_address+"'", (response))
	
