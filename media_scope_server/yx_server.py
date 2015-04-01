import time, os, copy, sys, random,threading
import BaseHTTPServer, urlparse, cgi,urllib, urllib2
from xml.etree import ElementTree as ET
from multiprocessing import Process
from subprocess import call

HOST_NAME = open('./config/remote_host.info').read().rstrip()
PORT_NUMBER = int(open('./config/yx_server_port.info').read().rstrip())

DBNAME = "medusa"
DB_ACCOUNT = (open('./config/db_account.info').read().rstrip()).split('|')
DB_USERNAME = DB_ACCOUNT[0]
DB_PASSWORD = DB_ACCOUNT[1]
DB_HOST = open('./config/db_host.info').read().rstrip()

Uploaded  = {}
SPD = {}
TM = {}

def getfile(fl):
	global Uploaded, SPD, TM
	time_log = threading.local()
	time_log.s = ''
	time_log.s += str(time.time()) + "\t(Y)notifiction received \r\n"	
	flag = 0
	pair = fl.popitem()
	#print "pair =  "+pair[1][0]
	#t_filename = "%s%s" % (str(int(random.random()*10000)), pair[0])
	if pair[0] != '':
		print pair[0]
		name_uids = pair[0].split('=')
		uids = name_uids[1].split('|')
		for i in range(len(uids)):
			download_urls = pair[1][0].split(",")
		con, cur = sql_execute2()
		for i in range(len(download_urls)):
			download_url = download_urls[i]
			print download_url 
			filename = name_uids[0]+'='+uids[i]#+'='+name_uids[-1] 
			ext = download_url.split('.')[-1]
			download_url = "http://"+download_url 
			
			if ext == 'txt':
				filename = './meta/' + filename
				urllib.urlretrieve(download_url, filename)
				f = open(filename, 'r')
				line = f.readline()
				
				if line[:4] != 'none':
					# sql_in = "INSERT INTO Meta_data (user, uid, feature, longtitude, latitude, time, size ) VALUES (" + line[:-1] +");"
					sql_in = "INSERT INTO Meta_data (user, uid, feature, longtitude, latitude, time, size, file_name, carDetectionNum, faceDetectionNum, blur,sceneTag, AngleOfView, lightIntensity, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, bearing_x, bearing_y, bearing_z, gps_lng, gps_lat, gps_acc) VALUES (" + line[:-1] +");"
					print "sql_a= " + sql_in
				#	con, cur = sql_execute(sql_in)
					cur.execute(sql_in)
					line = f.readline()
					while line:
						sql_in = "INSERT INTO Meta_data (user, uid, feature, longtitude, latitude, time, size, file_name, carDetectionNum, faceDetectionNum, blur,sceneTag, AngleOfView, lightIntensity, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, bearing_x, bearing_y, bearing_z, gps_lng, gps_lat, gps_acc) VALUES (" + line[:-1] +");"
						print "sql_b= " + sql_in
						cur.execute(sql_in)
						line = f.readline()
				#	con.close()
				f.close()
			else:
				flag = 1
				filename = './query/'+filename
				print "Downloaded filepath: " + filename					
#				sql_get = ("select size from Meta_data where user = {0} and uid = {1}").format(name.uids[0], uids[i])
#				cur.execute(sql_get)
#				dat = cur.fetchone()
				urllib.urlretrieve(download_url, filename)
				#SIZE = 0
				print "Got file now !!! " + filename
				sql_up = ("update Meta_data set size = 0 where user = {0} and uid = {1}").format(name_uids[0],uids[i])
				print sql_up
#				cur.execute(sql_up)
				time_log.s += str(time.time()) + "\t(Y)fetched {0} \r\n".format(filename)
		con.commit()
		con.close()
	else:
		print 'No photo captured!'
		pass
	if flag == 1:
		pass

def sql_execute2():
	import MySQLdb as mdb
	con = None
	data = None
	try:
		con = mdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DBNAME)
		cur = con.cursor()
		#cur.execute(sqlstmt)
	except mdb.Error, e:
		#log("! get_raw_mysql_data() err %d: %s" % (e.args[0], e.args[1]))
		print "sql_execute error"
	return con, cur

def sql_execute( sqlstmt):
	import MySQLdb as mdb
	con = None
	data = None
	try:
		con = mdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DBNAME)
		cur = con.cursor()
		cur.execute(sqlstmt)
	except mdb.Error, e:
		#log("! get_raw_mysql_data() err %d: %s" % (e.args[0], e.args[1]))
		print "sql_execute error"
	return con, cur
	
class FileHandler(threading.Thread):
	def run(self):
		getfile(self.fl)
	def __init__(self, fl):
		threading.Thread.__init__(self)
		self.fl = fl

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_POST(self):
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			content = self.rfile.read(length)
			print "received: "+content
			postvars = cgi.parse_qs(content, keep_blank_values=1)
			print postvars
			t = FileHandler(postvars)
			t.start()
#			getfile(postvars)
		else:
			postvars = {}
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		
def runMultiQueryServer():
	call(["python", "./multi_query.py"])

if __name__ == '__main__':

	## Start the Medusa Web Socket Server (php): 
	mqsproc = Process(\
		target=runMultiQueryServer, \
		name="MultiQueryServer"
	)
	mqsproc.daemon = True
	mqsproc.start()

	# start the Media Scope yx_server
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	thr.stopIt = True
	httpd.server_close()

	mqsproc.terminate()
	mqsproc.join()

	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
