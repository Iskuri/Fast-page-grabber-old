import pycurl
import cStringIO

class CurlHandler:

	#def __init__(self):

	def getResponse(self, ip_address):

		c = pycurl.Curl()
		
		try:
			c.setopt(c.URL, 'https://'+ip_address)
			buf = cStringIO.StringIO()
			c.setopt(c.WRITEFUNCTION, buf.write)
			c.setopt(c.SSL_VERIFYPEER, 0)
			c.setopt(c.SSL_VERIFYHOST, 0)
			c.setopt(c.NOSIGNAL, 1)
			c.setopt(c.CONNECTTIMEOUT, 30)
    			c.setopt(c.TIMEOUT, 30)
			c.perform()
			response = buf.getvalue()
			buf.close()
			#print response
			return response
		except:
			return ''
