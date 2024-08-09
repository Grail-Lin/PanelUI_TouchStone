#!/bin/bash
SERVICE="start.sh"
if pgrep -x "$SERVICE" > /dev/null
then
	echo "$SERVICE is running"
else
	echo "$SERVICE stopped"
	/home/cobio/co_dev/startup/start.sh &
fi


