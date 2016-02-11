#!/bin/bash
cd /local/share/ic_twitter/
source venv/bin/activate
cd -

python kill_ongoing_streams.py ongoing_streams.pid
rm ongoing_streams.pid
