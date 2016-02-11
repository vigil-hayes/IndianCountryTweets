import os
import csv
import sys
import logging

pidfile=sys.argv[1]

# Open the pidfile and go through each
# line, calling kill on each
with open(pidfile, "r") as pf:
	reader = csv.reader(pf, delimiter="\t")
	for row in reader:
		try:
			pid=int(row[0])
			print(pid)
			os.kill(pid, 9)
		except Exception as e:
			print(e)
			continue
