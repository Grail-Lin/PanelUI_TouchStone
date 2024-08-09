#!/bin/bash
SERVICE="Xwayland"
if pgrep -x "$SERVICE" > /dev/null
then
	echo "$SERVICE is running"
	pkill "$SERVICE"
else
	echo "$SERVICE stopped"
	#/home/cobio/co_dev/startup/start.sh &
fi


