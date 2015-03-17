# Import the relevant libraries
import urllib2
import math
import MySQLdb
import json

DBNAME = "medusa"
DB_ACCOUNT = (open('./config/db_account.info').read().rstrip()).split('|')
DB_USERNAME = DB_ACCOUNT[0]
DB_PASSWORD = DB_ACCOUNT[1]
DB_HOST = open('./config/db_host.info').read().rstrip()

def create_json():

  # Connect to the MySQL database
  db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DBNAME)

  # Creation of a cursor
  cursor = db.cursor()

  # Execution of a SQL statement
  query = ("select * from Meta_data")
  print query
  cursor.execute(query)

  # Get the total number of rows
  numrows = int (cursor.rowcount)
  print "numrows = ", numrows

  # Get and display the rows one at a time
  for i in range (numrows):
    row = cursor.fetchone()
    if (row):
      #print row[0], row[1], row[2]
      if (1):
        # print i,
        # print "latitude = ", row[4], "longitude = ", row[3]
        json_Landmark = queryGooglePlace(row[4], row[3], row[16], row[17])
          # Note: need to add unique photo_id, instead of using i...
        json_data = { "photoID" : i,
                      "user" : row[0],
                      "ceddValue" : row[2],
		      "location" : {
				"lat" : row[4],
				"lon" : row[3]
		      },
                      "gpsAccuracy" : row[22],
                      "timestamp" : row[5],
                      "photoSize" : row[6],
                      "carDetectionNum" : row[7],
                      "faceDetectionNum" : row[8],
                      "lightIntensity" : row[9],
                      "angleOfView" : row[16],
                      "azimuth" : row[17],
                      "pitch" : row[18],
                      "roll" : row[19],
                      "landmarkMeta" : json_Landmark
                      }
        print json.dumps(json_data, indent=4, separators=(',', ': '))

def queryGooglePlace(latSource, lngSource, aovSource, bearingSource):

  if latSource is None:
    #print "fuck!"
    return {'visibleLandmark' : []}

  if lngSource is None:
    #print "fuck!"
    return {'visibleLandmark' : []}

  if aovSource is None:
    #print "fuck!"
    return {'visibleLandmark' : []}

  if bearingSource is None:
    #print "fuck!"
    return {'visibleLandmark' : []}

  # Set the Places API key for your application
  AUTH_KEY = 'AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY'

  LOCATION_aov = float(aovSource)*180/math.pi

  # Define the location coordinates
  # By using [:-1] to delete '\n' of each readline()
  LOCATION_lat = str(latSource)
  LOCATION_lng = str(lngSource)
  LOCATION_bearing = str(bearingSource)

  # I use bearing direction with counter-clockwise
  LOCATION_bearing = float(LOCATION_bearing)
  if LOCATION_bearing > 90.0 :
    LOCATION_bearing = LOCATION_bearing - 270.0
  else :
    LOCATION_bearing = LOCATION_bearing + 90.0

  lat1=float(LOCATION_lat)
  lng1=float(LOCATION_lng)  

  # Define the radius (in meters) for the search
  RADIUS = '70' 

  # Compose a URL to query a predefined location with a radius of 5000 meters
  url = ('https://maps.googleapis.com/maps/api/place/search/json?location=%s,%s&radius=%s&key=%s') % (LOCATION_lat, LOCATION_lng, RADIUS, AUTH_KEY) 

  # Send the GET request to the Place details service (using url from above)
  response = urllib2.urlopen(url) 

  # Get the response and use the JSON library to decode the JSON
  json_raw = response.read()
  json_data = json.loads(json_raw)  

  json_Landmark = {'visibleLandmark' : []}

  # Iterate through the results and print them to the console
  if json_data['status'] == 'OK':
    #print 'It worked!'
    #file_out.write('*****'+target_name+'*****'+'\t'+LOCATION_lat+','+LOCATION_lng+'\t'+str(LOCATION_bearing))
    #file_out.write("\nthese buildings should be within the angle of view\n")
    for place in json_data['results']:
      lat2=float(place['geometry']['location']['lat'])
      lng2=float(place['geometry']['location']['lng'])
      y=math.sin(lng2-lng1)*math.cos(lat2);
      x=math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lng2-lng1)
      bearing=math.degrees(math.atan2(y,x))
      #if abs(bearing - LOCATION_bearing) < LOCATION_aov/2 :
      #perspective=math.tan((bearing-LOCATION_bearing)*math.pi/180)/math.tan((LOCATION_aov/2)*math.pi/180)
      #perspective=0.5*(perspective+1)
      #perspective=(1 - perspective)*28
      json_Landmark['visibleLandmark'].append({
						'landmarkName' : place['name'], 
						'location' : {
							'lat' : str(lat2), 
							'lon' : str(lng2)
						}
					})
      #file_out.write('\t'+place['name']+'\t'+str(lat2)+','+str(lng2)+'\t'+str(bearing)+'\t'+str(perspective)+'\n')
    #if abs(bearing - LOCATION_bearing) < LOCATION_aov :
        # print place['name'], ' : ', bearing, bearing - LOCATION_bearing
      #file_out.write('\t'+place['name']+'\t'+str(bearing)+'\n')
  #file_out.close()
  return json_Landmark

if __name__ == '__main__':
  create_json()
