import time, os, copy, sys, random, threading, errno, datetime, copy, operator
import BaseHTTPServer, urlparse, cgi,urllib, urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from threading import Thread
import threading
from xml.etree import ElementTree as ET

file_name = sys.argv[1]
PORT = 77779

log_file = open("../log/experiment" + str(datetime.datetime.utcfromtimestamp(int(time.time() - 7*3600))), "w")

def http_client(d):
	URL='http://204.57.0.100:' + str(PORT)
	req = urllib2.Request(URL, urllib.urlencode(d))
	u = urllib2.urlopen(req)
	

if __name__ == '__main__':
  	os.system("rm ../query/*")
  	
  	f = open(file_name, 'r')
	http_client([(file_name+'.xml', f.read())])
	f.close()
	
	ori_xml = ET.parse(file_name)
	input = ori_xml.findall('app/input')
	root = ori_xml.find('app')
	
	pending_photo = {}
	for i in input:
		wid = i.findtext('wwid')
		root.remove(i)
		t_uids = i.findtext('gvar')
		t_uids = (t_uids.split('='))[1]
		uids = t_uids.split('|')
		for j in range(len(uids)):
			id_credit = uids[j].split(':')
			pending_photo[wid+'='+id_credit[0]] = [int(id_credit[2]), int(id_credit[1])]
			
	time.sleep(2)
	
	t = 0
	total_credit = 0
	print pending_photo
	while (len(pending_photo) > 0):
	  	t = t + 1
		time.sleep(1)
		credit = 0
		filenames = ''
		got_filenames = ''
		del_keys = []
		flag = 0
		for k,v in pending_photo.iteritems():
			if (v[0] == t):
				flag = 1
				if (os.path.exists('../query/' + k)):
					credit += v[1]
					got_filenames += " " + k + "[" + str(v[1]) + "]"
				filenames += " " + k + "[" + str(v[1]) + "]"
				del_keys.append(k)
		if (flag==0):
			continue
		for k in del_keys:
			del pending_photo[k]
		print filenames + "(" + got_filenames+"): " + str(credit)
		log_file.write(filenames + "(" + got_filenames+"): " + str(credit) + '\r\n')
		total_credit += credit
	print "Total credit: " + str(total_credit)
	log_file.write("Total credit: " + str(total_credit) + '\r\n')
	log_file.close()
	

		
	
