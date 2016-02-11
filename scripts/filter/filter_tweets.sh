#!/bin/bash
cd /local/share/ic_twitter/
source venv/bin/activate
cd -

DATE="$(date +'%Y-%m-%d')"
HOUR="$(date +'%H')"

# For all unprocessed, collected tweets today
for log in /local/share/ic_twitter/scripts/collect/logs/"$DATE"/ic_*.json; do
	# Get the basename
	BASE=$(basename $log)
	# Remove duplicates
	awk '!a[$0]++' $log > "$BASE"
	rm $log
		
	# Filter tweets by location
	mkdir /local/share/ic_twitter/tweets/"$DATE"
	python filter_to_ic.py /local/share/ic_twitter/data/Gaz_aiannhr.txt "$BASE" /local/share/ic_twitter/tweets/"$DATE"/"$BASE"

done

# For all unprocessed, collected tweets today
for log in /local/share/ic_twitter/scripts/collect/logs/"$DATE"/*s_*.json; do
        # Get the basename
        BASE=$(basename $log)
        # Remove duplicates
        awk '!a[$0]++' $log > "$BASE"
        rm $log

        # Filter tweets by location
	mkdir /local/share/ic_twitter/tweets/"$DATE"
	mv "$BASE" /local/share/ic_twitter/tweets/"$DATE" 
done
