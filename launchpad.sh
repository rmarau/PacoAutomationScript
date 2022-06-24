#!/bin/sh


#docker run --rm -i -t -p 4444:4444 -p 7900:7900 --shm-size="2g" rmarau/liveselenium
echo "##################################################################"
echo "The script runs in a FIREFOX instance within the docker container.\nFollow up: http://localhost:7900   password:'secret'"
echo "##################################################################"

nohup /opt/bin/entry_point.sh </dev/null >/dev/null 2>&1 &

exec ~/run.sh