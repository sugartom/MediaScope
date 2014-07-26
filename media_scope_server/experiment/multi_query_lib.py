import random, urlparse, urllib, urllib2, sys, math, datetime, time, copy, os
from urllib2 import Request, urlopen, URLError, HTTPError
from googlemaps import GoogleMaps
import mst, kmeans_new, represent

ACCEPTOR_PORT = 77779
C2DM_M_S = open('../config/c2d_messaging_system.info').read().rstrip()

def select(paras):
	gmaps = GoogleMaps()
        address = paras['street']+", "+ paras['city']+", "+paras['state']
        latitude, longtitude = gmaps.address_to_latlng(address)
        print "Location convertion: " + str(latitude) + str(longtitude)
        time_start_mon = int(paras['s_mon'])
        time_start_day = int(paras['s_day'])
        time_start_hour = int(paras['s_hou'])
        time_end_mon = int(paras['e_mon'])
        time_end_day = int(paras['e_day'])
        time_end_hour = int(paras['e_hou'])
        radius = paras['r']
        start_time = datetime.datetime(2012, time_start_mon, time_start_day, time_start_hour, 0)
        end_time = datetime.datetime(2012, time_end_mon, time_end_day, time_end_hour, 0)
        start_epoch_time = time.mktime(start_time.timetuple()) * 1000
        end_epoch_time = time.mktime(end_time.timetuple()) * 1000
        distance = "3959*acos((sin({3}/57.29577951)*sin(latitude/57.29577951)+cos({3}/57.29577951)*cos(latitude/57.29577951)*cos(abs(longtitude-({2}))/57.29577951))) <{4}"
	querystr = ("select user, uid, feature, longtitude, latitude, time, size from Meta_data where time >= {0} and time <= {1} and " + distance + " order by user;").format(start_epoch_time, end_epoch_time, longtitude, latitude, radius)
	
	if (paras['r'] == '0'):
		querystr = ("select user, uid, feature, longtitude, latitude, time, size from Meta_data where time >= {0} and time <= {1} order by user;").format(start_epoch_time, end_epoch_time)
	print querystr	
	con, cur = sql_execute(querystr)
	
	data = []
	while True:
		dat = cur.fetchone()
		if dat == None:
			break
		data.append(dat)
	if (paras['type'] == '0'):
		return top_k_similar(data, paras['option1'], paras['option2'], paras['deadline'])
	if (paras['type'] == '1'):
		return mst.call_mst(data, paras['deadline'])
	if (paras['type'] == '2'):
		return kmeans_new.call_kmeans(data, paras['deadline'], int(paras['option1']))
	if (paras['type'] == '3'):
		return represent.call_represent(data, paras['deadline'], int(paras['option1']))
	else:
		return [], []
	pass
      
def top_k_similar(data, option1, option2, deadline):
	if (len(data) == 0):
		return ([], [])
	dist = []
	option1 = int(option1)
	
	query_image = []
	f = os.popen("java -jar ../libs/LIRE.jar QUERY_IMAGE/" + option2).read()
	f = f[:-1]
	query_image = [None]*7
	query_image[2]=(f)
	for i in range(len(data)):
		dist.append(pair_dist(data[i], query_image))
	
	self = dist.index(min(dist))
	del data[self]
	del dist[self]
	#print "first remove"+str(data[self][0])+" "+str(data[self][1])
	result = {}
	meta = {}
	total_dist = 0.0
	temp_dist = copy.deepcopy(dist)
	for i in range(min(option1, len(dist))):
		total_dist += 1.0/min(temp_dist)
		del temp_dist[temp_dist.index(min(temp_dist))]
	for i in range(min(option1, len(dist))):
		selected = dist.index(min(dist))
		if (not result.has_key(data[selected][0])):
			result[data[selected][0]] = ''
			meta[data[selected][0]] = ''
		result[data[selected][0]] += str(data[selected][1]) + ':' + str(int(1.0/dist[selected]/total_dist*1000.0)) + ':' + deadline + '|'
		meta[data[selected][0]] += str(data[selected][1]) + ',' + str(data[selected][3]) + ',' + str(data[selected][4]) + ',' + str(data[selected][5]) + '|'
		del data[selected]
		del dist[selected]
	for i in result:
		result[i] = result[i][:-1]
	for i in meta:
		meta[i] = meta[i][:-1]
	return (result, meta)

def unique_id():
        return (str(int(time.time() * 10000)) + str(int(random.random()*10000)))

def generate_task_file(task_id, user, file_list):
	upload_xml_file = ''
	upload_xml_file += "<xml>\n\t<app>\n<input>\n"
        upload_xml_file += '\t\t<name>' + task_id + '</name>\n'
        upload_xml_file += '\t\t<rrid>AKIAIHXRZUV7K7Q7JZ7A</rrid>\n'
        upload_xml_file += '\t\t<wwid>'+user+'</wwid>\n'
        upload_xml_file += '\t\t<rrkey>ZDijBdROJrc6TViueBWYVhD5o8hSVzv9Civaj+Zl</rrkey>\n'
        upload_xml_file += '\t\t<timeout>7 hour</timeout>\n'
        upload_xml_file += '\t\t<cmdpush>' + C2DM_M_S + '</cmdpush>\n'
        upload_xml_file += '\t\t<gvar>GVARINPUT=' + file_list + '</gvar></input>\n'
	return upload_xml_file

def send_task(d):
        URL='http://204.57.0.100:'+str(ACCEPTOR_PORT)
        req = urllib2.Request(URL, urllib.urlencode(d))
        try:
                u = urllib2.urlopen(req)
        except URLError, e:
                print "Connection Refused, check server"
		return -1
	return 0
	
def get_feature(x):
	y = x.find('cedd')
	yy = x.find(' ', y+5)
	return x[yy+1:]

def pair_dist(A, B):
	f1 = A[2].split('|')
	f2 = B[2].split('|')
	min_dist = sys.float_info.max
	for ii in range(len(f1)):
		for jj in range(len(f2)):
			f1_ = get_feature(f1[ii]).split(' ')
			f2_ = get_feature(f2[jj]).split(' ')
			temp = cedd_dist(f1_, f2_)
			if (temp < min_dist):
				min_dist = temp
	return min_dist
	
def matrix_dist(A):

#	face_diff = []
        time_diff = []
        distance_diff = []
        diff = []
        feature_diff = []
        for i in range(len(A)):
                for j in range(len(A)):
#                       face_diff.append(math.pow(int(A[i][2])-int(A[j][2]),2))
#                       car_diff.append(math.pow(int(A[i][3])-int(A[j][3]),2))
                        time_diff.append(math.pow(long(A[i][5])-long(A[j][5]),2))
#                        distance_diff.append(math.pow(A[i][3]-A[j][3],2)+math.pow(A[i][4]-A[j][4],2))
			distance_diff.append(0)
			f1 = A[i][2].split('|')
			f2 = A[j][2].split('|')
			min_dist = sys.float_info.max
			for ii in range(len(f1)):
				for jj in range(len(f2)):
					f1_ = get_feature(f1[ii]).split(' ')
					f2_ = get_feature(f2[jj]).split(' ')
					temp = cedd_dist(f1_, f2_)
					if (temp < min_dist):
						min_dist = temp
                        feature_diff.append(min_dist)

#       face_max = max(face_diff) if max(face_diff)!=0 else sys.maxint
#       car_max = max(car_diff) if max(car_diff)!=0 else sys.maxint
        time_max = max(time_diff) if max(time_diff)!=0 else sys.maxint
        distance_max = max(distance_diff) if max(distance_diff)!=0 else sys.maxint
        feature_max = max(feature_diff) if max(feature_diff)!=0 else sys.maxint
#       alpha_face = 1.0
        alpha_time = 1.0
#       alpha_car = 1.0
        alpha_distance = 1.0
        alpha_feature = 1.0
        for i in range(len(time_diff)):
                diff.append(alpha_distance*distance_diff[i]/distance_max+alpha_time*time_diff[i]/time_max+alpha_feature*feature_diff[i]/feature_max)
	return diff

def cedd_dist(f1, f2):
	f1_len = len(f1)
	f2_len = len(f2)
	if f1_len != f2_len:
		print "length not equal, please check!"
		return sys.float_info.max 
	else:
		for i in range(f1_len):
			f1[i] = float(f1[i])
			f2[i] = float(f2[i])
		t_sum1 = sum(f1)
		t_sum2 = sum(f2)
		Result = 0
		if t_sum1 == 0 or t_sum2 == 0:
			Result = 100
		elif t_sum1 == 0 and t_sum2 == 0:
			Result = 0
		else:
			tc1 = 0
			tc2 = 0
			tc3 = 0
			for i in range(f1_len):
				tc1 = tc1 + 1.0*f1[i]*f2[i]/(t_sum1*t_sum2)
				tc2 = tc2 + 1.0*f1[i]*f1[i]/(t_sum1*t_sum1)
				tc3 = tc3 + 1.0*f2[i]*f2[i]/(t_sum2*t_sum2)
			Result = (100 - 100 * tc1/(tc2+tc3-tc1))
		return max(0, Result)

def sql_execute( sqlstmt):
	import MySQLdb as mdb
	con = None
	data = None
	host = "localhost"
	dbname = "medusa"
	try:
		con = mdb.connect(host, 'root', 'xx', dbname)
		cur = con.cursor()
		cur.execute(sqlstmt)
	except mdb.Error, e:
		#log("! get_raw_mysql_data() err %d: %s" % (e.args[0], e.args[1]))
		print "sql_execute error"
	return con, cur
	

