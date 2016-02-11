#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import geopy
import geopy.distance
import math
import sys
import os
import datetime
import logging
import json

# Config file
configfile = sys.argv[1]

# Actor config file
tagfile = sys.argv[2]


# Rez bounding boxes
rez_BB = []

# Writes process to file
def writePidFile():
	try:
        	pid = str(os.getpid())
        	f = open('ongoing_streams.pid', 'a')
        	f.write("%s\n" % pid)
        	f.close()
		return
	except Exception as e:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		logging.info('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
		sys.exit(1)

# Sets up logs
def setUpLogs():
	# Make log directory
	try:
		os.mkdir("/local/share/ic_twitter/scripts/collect/logs/%s" % datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
	except Exception as e:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		logging.info('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))

	# Log file
	try:
		hour = datetime.datetime.strftime(datetime.datetime.now(), '%H')
                next_hour = int(hour)+1
                if next_hour == 24:
                        next_hour=1
		logfile = "logs/%s/%s.json" % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'), 'tags_%s' % next_hour)
		return logfile
	except Exception as e:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		logging.warning('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
		sys.exit(1)

# Set up configs
def setUpConfig():
	try:
		with open(configfile, 'r') as cf:
			config = json.load(cf)

			#Variables that contains the user credentials to access Twitter API 
			access_token = config["access_token"]
			access_token_secret = config["access_token_secret"]
			consumer_key = config["consumer_key"]
			consumer_secret = config["consumer_secret"]
			return [access_token, access_token_secret, consumer_key, consumer_secret]
	except Exception as e:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
                logging.warning('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
                sys.exit(1)

#This is a basic listener that writes to log file
class StdOutListener(StreamListener):
    logfile=""
    def set_logfile(self, lf):
	self.logfile = lf
	return

    def on_data(self, data):
	with open(logfile, 'a') as lf:
		lf.write(data)
        return True

    def on_error(self, status):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.warning('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), status))
	sys.exit(1)

def getOauthToken(app_key, app_secret):
	twitter = Twython(app_key, app_secret, oauth_version=2)
	return twitter.obtain_access_token()

def getTags(tagfile):
	try:
		tags = []
		with open(tagfile, 'r') as acf:
			rows = csv.reader(acf, delimiter="\t")
			for row in rows:
				tag = row[0]
				tags.append(tag)
		return tags
	except Exception as e:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        	logging.warning('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
       	 	sys.exit(1)
if __name__ == '__main__':

    # Twitter variables
    access_token = ""
    access_token_secret = ""
    consumer_key = ""
    consumer_secret = ""
    oath_token = ""

    # Set up log files
    logfile=setUpLogs()
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "Set up logs successfully"))
    # Set up config files
    access_token, access_token_secret, consumer_key, consumer_secret = setUpConfig()
    logging.debug('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "Set up config file successfully"))
    # Start PID file
    writePidFile()
    logging.debug('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "Set up PID file successfully"))
    
    l = StdOutListener()
    l.set_logfile(logfile)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    logging.debug('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "Twitter stream set up and authorized"))
    
    try:
	# Get tags
	tags=getTags(tagfile)
	print(tags)
	stream.filter(track=tags)

    except Exception as e:
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.warning('%s\t%s' % (datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), e))
	sys.exit(1)
