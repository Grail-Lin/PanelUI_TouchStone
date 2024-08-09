#!/bin/sh

if [ -z "$XDG_RUNTIME_DIR" ]; then
	XDG_RUNTIME_DIR="/tmp/$(id -u)-runtime-dir"

	mkdir -pm 0700 "$XDG_RUNTIME_DIR"
	export XDG_RUNTIME_DIR
fi

if [ -z "$DISPLAY" ]; then
	DISPLAY=":0"
fi


/bin/Xwayland &

cd /home/cobio/co_dev/PanelUI_TouchStone
python3 ./panel_demo.py

