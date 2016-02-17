import csv
import sys
import json
import geopy
import geopy.distance
import math
import datetime
import logging

rez_BB=[]

# determine if a point is inside a rectangle
# rect is defined by a list of coordinates representing
# the southernmost, westernmost, northernmost, easternmost points
# x is longitude (east/west), y is latitude (north/south)
def point_in_box(x, y, rect):
	inside=False
	west = rect[0]
	south = rect[1]
	east = rect[2]
	north = rect[3]	

	
	if x < west:
		return inside
	elif x > east:
		return inside
	elif y > north:
		return inside
	elif y < south:
		return inside
	else:
		return True

# Given a central latitude, longitude, and distance in miles
# return a list of 4 coordinates that represent
# the SW lng, SW lat, NE lng, NE lat
def getBoundingBox(lat, lng, dist, name):
        start = geopy.Point(lat, lng)

        # Define a general distance object
        d = geopy.distance.VincentyDistance(miles = math.sqrt(dist/float(2))) 
    
        # Create the bounding box with the southwest coordinates first
        bb= [d.destination(point=start, bearing=225).longitude, d.destination(point=start, bearing=225).latitude, d.destination(point=start, bearing=45).longitude, d.destination(point=start, bearing=45).latitude, name]
        return bb

# Add a bounding box to the list of rez bounding boxes
def addBoundingBox(bb):
        rez_BB.append(bb) 

# Reads in the rez_loc_filename and 
# creates a list of long lat bounding boxes
# for all indigenous territory
def getRezLocations(filename):
        with open(filename, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter="\t")
                for row in reader:
                        # GEOID   ANSICODE        NAME    POP10   HU10    ALAND   AWATER  ALAND_SQMI      AWATER_SQMI     INTPTLAT        INTP    TLONG
                        try:
                                house = float(row[4])
                                if house > 1000:
                                        lat = float(row[9].strip())
                                        lng = float(row[10].strip())
                                        sqmi = float(row[7].strip())
					name = row[2]
                                        bb = getBoundingBox(lat, lng, sqmi, name)
                                        addBoundingBox(bb)
                        except Exception as e:
				logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
                		logging.info('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
				continue

if __name__ == '__main__':
	tweet_coords={}

	# Get file names
	rez_data = sys.argv[1]
	tweets_data_path = sys.argv[2]
	logfile = sys.argv[3]

	# Populate the rez_BB
	# rez_BB is a list of lists of
	# S W  N E coordinates
	getRezLocations(rez_data)

	# Get all the tweets with geodata
	tweets_data = {}
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
    		try:
        		tweet = json.loads(line)
			tid = tweet["id"]
			tweets_data[tid]=line
        		if "null" in tweet["geo"] or "None" in tweet["geo"]:
                		continue
        		points=(tweet["coordinates"]["coordinates"])
			tweet_coords[tid]=points
    		except:
        		continue

	# Now go through all tweet_coords and see
	# if they exist in ANY of the rez locations in rez_BB
	# W S E N
	for tid in tweet_coords.keys():
		for rez in rez_BB:
			# W, S, E, N
			if point_in_box(tweet_coords[tid][0],tweet_coords[tid][1],rez):
				jsont=json.loads(tweets_data[tid])
				jsont["rez"] = rez[4]
				try:
					with open(logfile, 'a') as lf:
						lf.write("%s\n" % json.dumps(jsont, ensure_ascii=True))
				except Exception as e:
					logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
                                	logging.info('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
				break
				
