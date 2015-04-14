import time, os, copy, sys, random, threading, errno, datetime, copy, operator
import BaseHTTPServer, urlparse, cgi,urllib, urllib2, multi_query_lib
from urllib2 import Request, urlopen, URLError, HTTPError
from googlemaps import Client

HOST_NAME = open('./config/remote_host.info').read().rstrip()
HOST_PORT = int(open('./config/img_query_port.info').read().rstrip())
C2DM_M_S = open('./config/c2d_messaging_system.info').read().rstrip()
MSS_PATH = open('./config/media_scope_server_path.info').read().rstrip()

active_queries = {'0' : 'Empty Query Set'}
pending_task = {}
pending_photo = {}

def accept_query(qid, paras):
        global pending_photo, pending_task
        pending_task[qid] = {}
	pending_photo[qid] = {}

	result = multi_query_lib.select_id(paras)

        print "accept_query: result returned from select =========================="
        print "result = "+str(result)
        # print "meta = "+str(meta)
        if (len(result)) == 0:
                return
        f = open('upload_xml','r')
	upload_xml_file = ''
        upload_xml_file += "<xml>\n\t<app>\n"

	for user in result:
                task_id = "PHOTO_UPLOAD_" + multi_query_lib.unique_id()
		print "=="+str(user)+str(result[user])
                upload_xml_file += "<input>\n" + multi_query_lib.generate_task_file(task_id, user, result[user])
		pending_task[qid][user] = [] 
                pending_task[qid][user].append(task_id)
                uids = result[user].split('|')
                #metas = meta[user].split('|')
                for i in range(len(uids)):
			only_uid = uids[i].split(':')
                        pending_task[qid][user].append(only_uid[0])
                        pending_photo[qid][user + '=' + only_uid[0]] = int(only_uid[1])
        upload_xml_file += f.read()
        print "accept_query: upload_xml_file to medusa =========================="
        print upload_xml_file
        if multi_query_lib.send_task([((C2DM_M_S + '_kill.xml'), upload_xml_file)]) == -1:
		print "Send upload task failed"	
        print "Pending photos: "+str(pending_photo)
        print "Pending tasks: "+str(pending_task)

def return_result(qid):
	global pending_photo, pending_task, active_queries
	
	temp_pending_photo = copy.deepcopy(pending_photo)
	for k,v in pending_photo[qid].iteritems():
        	if (os.path.exists('query/' + k)):
                        names = k.split('=')
                        pending_task[qid][names[0]].remove(names[1])
                        if (len(pending_task[qid][names[0]]) == 1):
                        	del pending_task[qid][names[0]]
	
	ret_val = ''
	if (len(pending_photo[qid]) == 0):
        	ret_val += "<h2>No relevent results.</h2>"
 	        del pending_photo[qid]
		del pending_task[qid]
		del active_queries[qid]
		return ret_val

	while (len(pending_photo[qid]) > 0):
		(k, v) = max(pending_photo[qid].iteritems(), key=operator.itemgetter(1))
        	temp = k.split('=')
        	print "return_result: k (returned image address to multi_query)=========================="
        	print k
                ret_val += "<td width=205>"
                if (os.path.exists('query/' + k)):
                	ret_val += "<img src=\"data:image/jpg;base64,{0}\" width=205>".format(open('query/' + k).read().encode('base64').replace('\n', ''))
                else:
                	ret_val += "<b>Warning:</b> Photo failed to be uploaded on time."
		del pending_photo[qid][k]
	ret_val += "</td>"
        del pending_photo[qid]
	del pending_task[qid]
	del active_queries[qid]
        print 'Finish response to ('+str(qid)+'). '
	print '    Now query set (' + str(active_queries)+')'
	print '    Pending photo ('+str(pending_photo)+')'
	print '    Pending task ('+str(pending_task)+')'
	return ret_val


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(self):
		url_content = urlparse.urlparse(self.path)
		query = url_content.query
		print "do_GET: query from web browser =========================="
		print query
		path = url_content.path
		if path != MSS_PATH:
			return
		args = query.split("&")
		paras = {}
		for i in range(len(args)):
			temp = args[i].split("=")
			if len(temp) >= 2:
				paras[temp[0]] = temp[1]
	        self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write("<html><body>")
		# self.wfile.write("Requested image ID is: " + str(paras)+"\r\n")
		if 'query_id' in paras:
			self.wfile.write(return_result(paras['query_id']))
		else:
			query_id = str(int(max(active_queries)) + 1)
			print "accepted query (" + str(query_id)+")"
			active_queries[query_id] = query

			accept_query(query_id, paras)

			# self.wfile.write("<Meta http-equiv=\"Refresh\" Content=\"" + "10" + "; url=http://" + HOST_NAME + ":" + str(HOST_PORT) + MSS_PATH + "?" + query + "&query_id=" + query_id + "\">")
			timer = 0
			rev_file_name = "NULL"
			if (len(paras["ID"].split('-')) > 1):
				rev_file_name = paras["ID"].split('-')[0] + paras["ID"].split('-')[-1]
				
			while (True):
				if (os.path.exists("query/" + paras["ID"])):
					self.wfile.write("http://" + HOST_NAME + "/tom_www/MediaScope/media_scope_server/query/" + paras["ID"])
					break
				elif (os.path.exists("query/" + rev_file_name)):
					self.wfile.write("http://" + HOST_NAME + "/tom_www/MediaScope/media_scope_server/query/" + rev_file_name)
					break
				timer += 1
				if (timer >= int(paras["timeout"])):
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
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
