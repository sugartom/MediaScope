'''
  Author: Xiaochen Liu
  Date: Apr 10, 2015
  Function: Reply user request with the demanded image's URL or "timeout"
'''

import time, os, copy, sys, random, threading, errno, datetime, copy, operator
import BaseHTTPServer, urlparse, cgi,urllib, urllib2, multi_query_lib
from urllib2 import Request, urlopen, URLError, HTTPError
from googlemaps import Client

HOST_NAME = open('./config/remote_host.info').read().rstrip()
HOST_PORT = int(open('./config/img_query_port.info').read().rstrip())
C2DM_M_S = open('./config/c2d_messaging_system.info').read().rstrip()
MSS_PATH = open('./config/media_scope_server_path.info').read().rstrip()

pending_task = {}
pending_photo = {}

def accept_query(qid, paras): # function for sending query to Medusa
        global pending_photo, pending_task
        pending_task[qid] = {}
	pending_photo[qid] = {}

	result = multi_query_lib.select_id(paras) # get parameters of the image (like uid, lat, lng, time, etc.)

        print "accept_query: result returned from select =========================="
        print "result = "+str(result)
        
        if (len(result)) == 0:
                return
                
        f = open('upload_xml','r') # generate the query xml that should be sent to Medusa
	upload_xml_file = ''
        upload_xml_file += "<xml>\n\t<app>\n"
	for user in result:
                task_id = "PHOTO_UPLOAD_" + multi_query_lib.unique_id()
		print "=="+str(user)+str(result[user])
                upload_xml_file += "<input>\n" + multi_query_lib.generate_task_file(task_id, user, result[user])
		pending_task[qid][user] = [] 
                pending_task[qid][user].append(task_id)
                uids = result[user].split('|')
                for i in range(len(uids)):
			only_uid = uids[i].split(':')
                        pending_task[qid][user].append(only_uid[0])
                        pending_photo[qid][user + '=' + only_uid[0]] = int(only_uid[1])
        upload_xml_file += f.read()
        print "accept_query: upload_xml_file to medusa =========================="
        print upload_xml_file
        
        if multi_query_lib.send_task([((C2DM_M_S + '_kill.xml'), upload_xml_file)]) == -1: # send the xml to Medusa
		print "Send upload task failed"	
        print "Pending photos: "+str(pending_photo)
        print "Pending tasks: "+str(pending_task)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
	def do_GET(self): # once the server receives user query
		url_content = urlparse.urlparse(self.path)
		query = url_content.query # get the query
		
		print "do_GET: query from web browser =========================="
		print query
		
		path = url_content.path
		if path != MSS_PATH:
			return
		args = query.split("&")
		paras = {}
		for i in range(len(args)): # get parameters from the URL of user query
			temp = args[i].split("=")
			if len(temp) >= 2:
				paras[temp[0]] = temp[1]
				
		# write the headers
	        self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write("<html><body>")

		# since Medusa will automatically remove the '-' in image names
		# so we need to match the requested name with both '-' added and not added.
		rev_file_name = "NULL"		
		if (len(paras["ID"].split('-')) > 1): # get the file name without '-'
			rev_file_name = paras["ID"].split('-')[0] + paras["ID"].split('-')[-1]
		
		# if image alread exists, return to the user
		if (os.path.exists("query/" + paras["ID"])):
			self.wfile.write("http://" + HOST_NAME + "/tom_www/MediaScope/media_scope_server/query/" + paras["ID"])
		elif (os.path.exists("query/" + rev_file_name)):
			self.wfile.write("http://" + HOST_NAME + "/tom_www/MediaScope/media_scope_server/query/" + rev_file_name)
			
		# else send query to Medusa to get the image
		else:	
			print "Image not cached. Try to send query to Medusa"
			accept_query(query_id, paras) # send query
		
			timer = 0 # set up timer
			while (True):
				if (os.path.exists("query/" + paras["ID"])): # compare image name
					self.wfile.write("http://" + HOST_NAME + "/tom_www/MediaScope/media_scope_server/query/" + paras["ID"])
					break
				elif (os.path.exists("query/" + rev_file_name)):
					self.wfile.write("http://" + HOST_NAME + "/tom_www/MediaScope/media_scope_server/query/" + rev_file_name)
					break
				timer += 1
				if (timer >= int(paras["timeout"])): # return "timeout" if timer expires
					self.wfile.write("timeout")
					break
				print "Looking for the image .......... " + str(timer)
				time.sleep(1)

		self.wfile.write("</body></html>")		

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, HOST_PORT), MyHandler)
	
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, HOST_PORT)
	
	try:
		httpd.serve_forever() # start the server at port 9999
	except KeyboardInterrupt:
		pass
	httpd.server_close()
