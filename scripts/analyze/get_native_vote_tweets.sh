#!/bin/bash
cd /local/share/ic_twitter/
source venv/bin/activate
cd -


# For all unprocessed, collected tweets today
for log in /local/share/ic_twitter/scripts/collect/logs/2016-02-*/tags*.json; do
	# Get the basename
	python get_native_vote_tweets.py $log nativevote.csv
done


