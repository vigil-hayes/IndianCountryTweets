#!/bin/bash

tags=$1
actors=$2
out=$3

# timestamp, tid, uid, uname, replytostatus, replytouser, oid, ouid, ufollowcount, ufriendcount, ufavecount, ustatuscount, lat, lng, ','.join(mentions), ','.join(hashtags), ','.join(urls), ','.join(media), timestamp-otimestamp, otimestamp, oufollowcount, oufriendcount, oufavecount, oustatuscount, olat, olng, text

echo "TAG: # Tweets" >> $out
awk 'BEGIN{FS="\t"}!a[$2]++' $tags | wc -l >> $out

echo "TAG: % Retweets" >> $out
awk 'BEGIN{FS="\t"}{tweets+=1; if($3 !~ $8){retweet+=1}}END{print retweet/tweets}' $tags >> $out

echo "TAG: % Replies" >> $out
awk 'BEGIN{FS="\t"}{tweets+=1; if($5 !~ /None/ || $6 !~ /None/){reply+=1}}END{print reply/tweets}' $tags >> $out

echo "TAG: # Unique users" >> $out
awk 'BEGIN{FS="\t"}!a[$3]++' $tags | wc -l >> $out

echo "TAG: # Unique content creators" >> $out
awk 'BEGIN{FS="\t"}{if($8 ~ /None/){a[$3]}else{a[$8]}}END{for(x in a){creator+=1}print creator}' $tags >> $out
echo "++++++++++++++++++++++++++++++++++++++" >> $out
echo "ACTOR: # Tweets" >> $out
awk 'BEGIN{FS="\t"}!a[$2]++' $actors | wc -l >> $out

echo "ACTOR: % Retweets" >> $out
awk 'BEGIN{FS="\t"}{tweets+=1; if($3 !~ $8){retweet+=1}}END{print retweet/tweets}' $actors >> $out

echo "ACTOR: % Replies" >> $out
awk 'BEGIN{FS="\t"}{tweets+=1; if($5 !~ /None/ || $6 !~ /None/){reply+=1}}END{print reply/tweets}' $actors >> $out

echo "ACTOR: # Unique users" >> $out
awk 'BEGIN{FS="\t"}!a[$3]++' $actors | wc -l >> $out

echo "ACTOR: # Unique content creators" >> $out
awk 'BEGIN{FS="\t"}{if($8 ~ /None/){a[$3]}else{a[$8]}}END{for(x in a){creator+=1}print creator}' $actors >> $out

echo "++++++++++++++++++++++++++++++++++++++" >> $out
# Combine
awk 'BEGIN{FS="\t"} FNR==NR{a[$2]=$0; next}{if(!($2 in a)){a[$2]=$0}}END{for(x in a){print a[x]}}' $tags $actors > combined.csv

echo "COMBINED: # Tweets" >> $out
awk 'BEGIN{FS="\t"}!a[$2]++' combined.csv | wc -l >> $out

echo "COMBINED: % Retweets" >> $out
awk 'BEGIN{FS="\t"}{tweets+=1; if($3 !~ $8){retweet+=1}}END{print retweet/tweets}' combined.csv >> $out

echo "COMBINED: % Replies" >> $out
awk 'BEGIN{FS="\t"}{tweets+=1; if($5 !~ /None/ || $6 !~ /None/){reply+=1}}END{print reply/tweets}' combined.csv >> $out


echo "COMBINED: # Unique users" >> $out
awk 'BEGIN{FS="\t"}!a[$3]++' combined.csv | wc -l >> $out

echo "COMBINED: # Unique content creators" >> $out
awk 'BEGIN{FS="\t"}{if($8 ~ /None/){a[$3]}else{a[$8]}}END{for(x in a){creator+=1}print creator}' combined.csv >> $out

