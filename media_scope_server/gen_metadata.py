import time, os, copy, sys, random,threading
import BaseHTTPServer, urlparse, cgi,urllib, urllib2
from xml.etree import ElementTree as ET
import multi_query_lib

SLEEP_INTERVAL = 6000
wids = (open('./config/wids.info').read().rstrip()).split(',')
ADDRESS_PORT = open('./config/mdscript_acceptor_address_port.info').read().rstrip()
C2DM_M_S = open('./config/c2d_messaging_system.info').read().rstrip()

def start_cal_metadata(wids):
	name = 'METADATA-GENERATOR'
	rid = 'AKIAIHXRZUV7K7Q7JZ7A'
	rkey = 'ZDijBdROJrc6TViueBWYVhD5o8hSVzv9Civaj+Zl'
	timeout = '7 hour'
	start_xml = C2DM_M_S + '_start.xml'
	f = open(start_xml,'w')
	f.write('<xml>\n\t<app>\n')
	for i in range(len(wids)):
		if wids[i] != '':
			sql_cmd = ("select max(uid) from Meta_data where user = \"{0}\"").format(wids[i])
			print sql_cmd
		        con, cur = multi_query_lib.sql_execute(sql_cmd)
		        dat = cur.fetchone()
	        	if dat[0] != None:
				gvar = dat[0]
		        else:
				gvar = 0
			gvar = 0
			print gvar
			f.write('\t\t<input>\n')
			f.write('\t\t<name>'+name+'</name>\n')
			f.write('\t\t<rrid>'+rid+'</rrid>\n')
			f.write('\t\t<rrkey>'+rkey+'</rrkey>\n')
			f.write('\t\t<wwid>'+str(wids[i])+'</wwid>\n')
			f.write('\t\t<gvar>GVARSTARTUID='+str(int(gvar) + 1)+'</gvar>\n')
			f.write('\t\t<timeout>'+timeout+'</timeout>\n')
			f.write('\t\t<cmdpush>'+C2DM_M_S+'</cmdpush>\n')
			f.write('\t\t</input>\n')
	fd = open('meta_xml2','r')
	f.write(fd.read())
	fd.close()
	f.close()
	f = open(start_xml,'r')
	http_client([(start_xml, f.read())])
	f.close()
	
def http_client(d):
	URL='http://' + str(ADDRESS_PORT)
	req = urllib2.Request(URL, urllib.urlencode(d))
	u = urllib2.urlopen(req)

if __name__ == '__main__':
	print wids
	while True:
		start_cal_metadata(wids)
		time.sleep(SLEEP_INTERVAL)
