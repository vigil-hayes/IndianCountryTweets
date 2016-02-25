#!/bin/bash

log=$1

awk 'BEGIN{FS="\t"}{if($7 ~ /None/ || $7 == ""){a[$2]+=1}else{a[$7]+=1}}END{for(x in a){print x "\t" a[x]}}' $log | sort -nrk 2 | sed -n 1,25p > "$log".top25
