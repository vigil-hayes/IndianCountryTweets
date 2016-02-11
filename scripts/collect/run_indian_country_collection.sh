#!/bin/bash
cd /local/share/ic_twitter/
source venv/bin/activate
cd -

python twitter_streaming_indian_country.py config/ic_keys.cfg /local/share/ic_twitter/data/Gaz_aiannhr.txt &>> logs/twitter_streaming_indian_country.log &
python twitter_streaming_indian_country.py config/ic_keys2.cfg /local/share/ic_twitter/data/Gaz_aiannhr.txt &>> logs/twitter_streaming_indian_country2.log & 
python twitter_streaming_indian_country.py config/ic_keys3.cfg /local/share/ic_twitter/data/Gaz_aiannhr.txt &>> logs/twitter_streaming_indian_country3.log &
python twitter_streaming_indian_country.py config/ic_keys4.cfg /local/share/ic_twitter/data/Gaz_aiannhr.txt &>> logs/twitter_streaming_indian_country4.log &
python twitter_streaming_indian_country.py config/ic_keys5.cfg /local/share/ic_twitter/data/Gaz_aiannhr.txt &>> logs/twitter_streaming_indian_country5.log &
python twitter_streaming_indian_country.py config/ic_keys6.cfg /local/share/ic_twitter/data/Gaz_aiannhr.txt &>> logs/twitter_streaming_indian_country6.log &

python twitter_streaming_native_actors.py config/actors_keys.cfg config/user_ids.json  &>> logs/twitter_streaming_native_actors.log &

python twitter_streaming_native_tags.py config/tags_keys.cfg config/native_tags.cfg &>> logs/twitter_streaming_native_tags.log &
