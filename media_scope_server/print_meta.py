# Import the relevant libraries
import urllib2
import math
import MySQLdb
import json
import sys

# pretty = str(raw_input("Do you want pretty output (y or n): "))
pretty = sys.argv[1]

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
  #print query
  cursor.execute(query)

  # Get the total number of rows
  numrows = int (cursor.rowcount)
  #print "numrows = ", numrows

  # Get and display the rows one at a time
  for i in range (numrows):
    row = cursor.fetchone()
    if (row):
      #print row[0], row[1], row[2]
      if (1):
        json_index = { "index" : { "_id" : str(i)}}
        if (pretty == "y"):
          print json.dumps(json_index, indent=4, separators=(',', ': '), sort_keys=True)
        else:
          print json.dumps(json_index, sort_keys=True)

        json_Landmark = queryGooglePlace(row[24], row[23], row[16], row[17])
        # Note: need to add unique photo_id, instead of using i...
        json_data = { "photoID" : i,
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
                      "landmarkMeta" : json_Landmark
                      }
    if (pretty == "y"):
      print json.dumps(json_data, indent=4, separators=(',', ': '), sort_keys=True)
    else:
      print json.dumps(json_data, sort_keys=True)

def queryGooglePlace(latSource, lngSource, aovSource, bearingSource):

  if latSource is None:
    return {'visibleLandmark' : []}

  if lngSource is None:
    return {'visibleLandmark' : []}

  if aovSource is None:
    return {'visibleLandmark' : []}

  if bearingSource is None:
    return {'visibleLandmark' : []}

  # Set the Places API key for your application
  AUTH_KEY = 'AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY'

  LOCATION_aov = float(aovSource)*180/math.pi

  # Define the location coordinates
  # By using [:-1] to delete '\n' of each readline()
  LOCATION_lat = str(latSource)
  LOCATION_lng = str(lngSource)
  LOCATION_bearing = float(str(bearingSource))

  # I use bearing direction with counter-clockwise
  LOCATION_bearing = calibrateBearing(LOCATION_bearing)
  # LOCATION_bearing = float(LOCATION_bearing)
  # if LOCATION_bearing > 90.0 :
  #   LOCATION_bearing = LOCATION_bearing - 270.0
  # else :
  #   LOCATION_bearing = LOCATION_bearing + 90.0

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

def calibrateBearing(inputBearing):
  if inputBearing > 90.0:
    return inputBearing - 270.0
  else:
    return inputBearing + 90.0

if __name__ == '__main__':
  create_json()
