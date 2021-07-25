#!/usr/bin/env bash
# Helper wrapper for scrcpy to allow for detecting whether the target is over wifi
#   or hardlines (usb cable) and optimizing the connection to match

set -euo pipefail

# Resolve the underlying binary
TGT_BIN="scrcpy"
if [[ "$(which $TGT_BIN)" != "$(which -a $TGT_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TGT_BIN | wc -l)
    BIN=$(which -a $TGT_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    BIN=$(which $TGT_BIN)
fi

# Ensure the adb server is up, otherwise subsequent command fails when the server
#   launches
adb start-server 1>/dev/null
# If args are passed, treat it as a straight passthrough
[[ "$#" != "0" ]] && exec $SCRCPY_BIN "$@"

DEVICES=$(adb devices | grep -e "device$" | awk '{ print $1 }')

if [[ "$(echo $DEVICES | head -n1)" == *":"* ]]; then
   exec $SCRCPY_BIN --bit-rate 2M --max-size 800 --max-fps 15
else
   exec $SCRCPY_BIN
fi
