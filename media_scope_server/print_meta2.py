import urllib2
import math
import MySQLdb
import json
import sys
import time
import utm

pretty = False

if len(sys.argv) > 1:
	if sys.argv[1] == 'y':
		pretty = True

timestr = time.strftime("%Y%m%d-%H%M%S")
f = open('./combined_meta/' + timestr + '.txt', 'w')

def sql_execute():

	DBNAME = "medusa"
	DB_ACCOUNT = (open('./config/db_account.info').read().rstrip()).split('|')
	DB_USERNAME = DB_ACCOUNT[0]
	DB_PASSWORD = DB_ACCOUNT[1]
	DB_HOST = open('./config/db_host.info').read().rstrip()

	try:
		# Connect to the MySQL database
		db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DBNAME)
		# Creation of a cursor
		cursor = db.cursor()
		# Execution of a SQL statement
		query = ("select distinct * from Meta_data")
		#print query
		cursor.execute(query)
		# Get the total number of rows
		numrows = int (cursor.rowcount)

	except MySQLdb.Error, e:
		print "sql_execute error!"

	return cursor, numrows

def create_json():

	cursor, numrows = sql_execute()

	# Get and display the rows one at a time
	for i in range(numrows):
		row = cursor.fetchone()
		if (row):
			json_index = { "index" : { "_id" : str(i)}}
			if pretty:
				f.write(json.dumps(json_index, indent=4, separators=(',', ': '), sort_keys=True) + '\n')
			else:
				f.write(json.dumps(json_index, sort_keys=True) + '\n')

			json_Landmark = queryGooglePlace(row[24], row[23], row[16], row[17])
			json_data = { 	"photoID" : i,
							"user" : row[0],
							"uid" : row[1],
							"ceddValue" : row[2],
							"location" : {
								"lat" : row[24],
								"lon" : row[23]
							},
							"gpsAccuracy" : row[25],
							"timestamp" : row[5],
							"photoSize" : row[6],
							"photoName" : row[7],
							"carDetectionNum" : row[8],
							"faceDetectionNum" : row[9],
							"blur" : row[10],
							"indoor" :row[11],
							"angleOfView" : row[12],
							"lightIntensity" : row[13],
							"azimuth" : row[20],
							"pitch" : row[21],
							"roll" : row[22],
							"acc_x" : row[14],
							"acc_y" : row[15],
							"acc_z" : row[16],
							"mag_x" : row[17],
							"mag_y" : row[18],
							"mag_z" : row[19],
							"landmarkMeta" : json_Landmark }

			if pretty:
				f.write(son.dumps(json_data, indent=4, separators=(',', ': '), sort_keys=True) + '\n')
			else:
				f.write(json.dumps(json_data, sort_keys=True) + '\n')

		else:
			print "fetchone error!"

# Need to be revised...
def calibrateBearing(inputBearing):
	return -20 - inputBearing

class point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

def distance(a, b):
	return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def queryGooglePlace(latSource, lngSource, aovSource, bearingSource):

	json_Landmark = {'visibleLandmark' : []}

	if (latSource is None) or (lngSource is None) or (aovSource is None) or (bearingSource is None):
		return json_Landmark

	# Set the Places API key for your application
	AUTH_KEY = 'AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY'

	LOCATION_aov = float(aovSource) * 180 / math.pi

	# Define the location coordinates
	LOCATION_lat = str(latSource)
	LOCATION_lng = str(lngSource)
	lat1=float(LOCATION_lat)
	lng1=float(LOCATION_lng)

	tmp = utm.from_latlon(lat1, lng1)
	photoLocation = point(tmp[0], tmp[1])
	zone_num = tmp[2]
	zone_letter = tmp[3]

	# Convert from lat-lng to x-y plane

	LOCATION_bearing = calibrateBearing(float(bearingSource))

	# Define the radius (in meters) for the search
	RADIUS = '70'

	# Compose a URL to query a predefined location with a radius of 5000 meters
	url = ('https://maps.googleapis.com/maps/api/place/search/json?location=%s,%s&radius=%s&key=%s') % (LOCATION_lat, LOCATION_lng, RADIUS, AUTH_KEY)

	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	# Iterate through the results and do something...
	if json_data['status'] == 'OK':
		for place in json_data['results']:
			lat2 = float(place['geometry']['location']['lat'])
			lng2 = float(place['geometry']['location']['lng'])

			tmp = utm.from_latlon(lat2, lng2)
			landmarkLocation = point(tmp[0], tmp[1])

			landmarkBearing = math.atan2(landmarkLocation.y - photoLocation.y, landmarkLocation.x - photoLocation.x) * 180 / math.pi

			if abs(landmarkBearing - LOCATION_bearing) < LOCATION_aov / 2:
				json_Landmark['visibleLandmark'].append({
					'landmarkName' : place['name'],
					'location' : {
						'lat' : str(lat2),
						'lon' : str(lng2)
					},
					'distance' : distance(photoLocation, landmarkLocation)
				})

	return json_Landmark

if __name__ == '__main__':	
	create_json()
	f.close()