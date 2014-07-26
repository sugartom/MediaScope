import time, os, copy, sys, random, threading, errno, datetime, copy, operator
import BaseHTTPServer, urlparse, cgi,urllib, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from threading import Thread
import threading
from xml.etree import ElementTree as ET

#queries = ["2_12", "0_8"]
queries = ["0_8"]

PORT = 77779

log_file = open("../log/experiment" + str(datetime.datetime.utcfromtimestamp(int(time.time() - 7*3600))), "w")

def http_client(d):
	URL='http://204.57.0.100:' + str(PORT)
	req = urllib2.Request(URL, urllib.urlencode(d))
	u = urllib2.urlopen(req)
	
def query_handler(filename):
	f = open(filename, 'r')
	local_data = threading.local()
	time_data = filename.split("_")
	time.sleep(int(time_data[0]))
	http_client([(filename+'.xml', f.read())])
	f.close()
	
	ori_xml = ET.parse(filename)
	input = ori_xml.findall('app/input')
	root = ori_xml.find('app')
	
	local_data.pending_photo = {}
	for i in input:
		wid = i.findtext('wwid')
		root.remove(i)
		t_uids = i.findtext('gvar')
		t_uids = (t_uids.split('='))[1]
		uids = t_uids.split('|')
		for j in range(len(uids)):
			id_credit = uids[j].split(':')
			local_data.pending_photo[wid+'='+id_credit[0]] = int(id_credit[1])
	
	print filename + ": " + str(local_data.pending_photo)
	log_file.write(filename + ": " + str(local_data.pending_photo) + '\r\n')
	time.sleep(int(time_data[1]))
	total_credit = 0
	for k,v in local_data.pending_photo.iteritems():
		if (os.path.exists('../query/' + k)):
			total_credit += v
	print filename + ": " + str(total_credit)
	log_file.write(filename + ": " + str(total_credit) + '\r\n')
	

if __name__ == '__main__':
	thread_handlers = []
	for f in queries:
		t = Thread(target=query_handler, args=(f, ))
		t.start()
		thread_handlers.append(t)
		
	for t in thread_handlers:
		t.join()
		
	log_file.close()
		
	
