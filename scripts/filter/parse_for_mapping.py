import json
import pandas as pd
import sys
import re

flag=0
tweets_data_path = sys.argv[1]

errlog="grab_location.error"

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
	tweet = json.loads(line)
	if "null" in tweet["geo"] or "None" in tweet["geo"]:
		continue
	hashtaglist=tweet["entities"]["hashtags"]
	htlist = ""
	for ht in hashtaglist:
		htlist += "#%s " % (ht["text"])
	taggeduserlst=tweet["entities"]["user_mentions"]
	tulist = ""
	for tu in taggeduserlst:
		tulist+= "@%s " % (tu["screen_name"])
	print("%s,%s,%s,%s,@%s,%s,%s,%s" % (tweet["rez"], tweet["coordinates"]["coordinates"][0], tweet["coordinates"]["coordinates"][1], tweet["created_at"], tweet["user"]["screen_name"], re.sub('[^A-Za-z0-9:\/.#@]+', ' ', tweet["text"].encode('ascii', 'ignore')), htlist, tulist))
    except Exception as e:
	print(e)
        continue

	
