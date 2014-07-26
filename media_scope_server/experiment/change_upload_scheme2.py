import time, os, copy, sys, random,threading
import BaseHTTPServer, urlparse, cgi,urllib, urllib2
from xml.etree import ElementTree as ET
import multi_query_lib

#wids = ["ENL1", "ENL2", "ENL3", "ENL4"]
wids = ["ENL1"]
PORT = 7777
HOST = "128.125.121.204"
SLEEP_INTERVAL = 6000
C2DM_M_S = open('./config/c2d_messaging_system.info').read().rstrip()

scheme = sys.argv[1]
window = sys.argv[2]
def start_cal_metadata(wids):
	name = 'METADATA-GENERATOR'
	rid = 'AKIAIHXRZUV7K7Q7JZ7A'
	rkey = 'ZDijBdROJrc6TViueBWYVhD5o8hSVzv9Civaj+Zl'
	timeout = '7 hour'
	start_xml = C2DM_M_S + '_start.xml'
	f = open(start_xml,'w')
	f.write('<xml>\n\t<app>\n')
	for i in range(len(wids)):
		f.write('\t\t<input>\n')
		f.write('\t\t<name>'+name+'</name>\n')
		f.write('\t\t<rrid>'+rid+'</rrid>\n')
		f.write('\t\t<rrkey>'+rkey+'</rrkey>\n')
		f.write('\t\t<wwid>'+str(wids[i])+'</wwid>\n')
		f.write('\t\t<gvar>GVARINPUT='+str(scheme)+'|'+str(window)+'</gvar>\n')
		f.write('\t\t<timeout>'+timeout+'</timeout>\n')
		f.write('\t\t<cmdpush>'+C2DM_M_S+'</cmdpush>\n')
		f.write('\t\t</input>\n')
	fd = open('upload_xml','r')
	f.write(fd.read())
	fd.close()
	f.close()
	f = open(start_xml,'r')
	http_client([(start_xml, f.read())])
	f.close()
	
def http_client(d):
	URL='http://' + HOST + ':' + str(PORT)
	req = urllib2.Request(URL, urllib.urlencode(d))
	u = urllib2.urlopen(req)

if __name__ == '__main__':
	print wids
	start_cal_metadata(wids)
