#!/usr/bin/python

import time, os, copy, sys, random, threading
import BaseHTTPServer, urlparse, cgi, urllib, urllib2
from os import path

ACCEPTOR_IP = 'http://' + open('./config/mdscript_acceptor_address_port.info').read().rstrip()
xml_file = sys.argv[1]
def run_xml():
	f = open(xml_file, 'r')
	http_client([(path.basename(xml_file), f.read())]) # ?<file_name>=<file_contents>
	f.close()
	
def http_client(d):
	req = urllib2.Request(ACCEPTOR_IP, urllib.urlencode(d))
	print "Request url: " + req.get_full_url()
	#print "Request payload: " + req.get_data()
	u = urllib2.urlopen(req)

if __name__ == '__main__':
	run_xml()
