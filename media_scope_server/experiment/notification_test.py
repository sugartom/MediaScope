import urllib2, urllib

file_name = "ENL1=555"
link = "128.125.121.204/medusa/tasktracker/data/99000028543438_39222175120130316_163049.jpg"

d= [(file_name, link)]
print "got single file:" +str(d)
req = urllib2.Request("http://128.125.121.204:9000", urllib.urlencode(d))
u = urllib2.urlopen(req)
