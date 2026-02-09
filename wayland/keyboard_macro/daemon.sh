#!/usr/bin/env bash

set -euo pipefail

HANDLER=/run/user/${UID}/run-macro
PIDFILE=/run/user/${UID}/macro-daemon.pidfile
LCLICK=0xC0

# Mark up/track pid for trigger coordination
echo $$ > $PIDFILE
# Remove handler if exists to start
if [[ -f $HANDLER ]]; then
    rm $HANDLER
fi

trap cleanup EXIT

cleanup() {
    echo "Closing, cleaning up state..."
    # Remove handler if exists to start
    if [[ -f $HANDLER ]]; then
        rm $HANDLER
    fi
    # Cleanup pidfile
    rm $PIDFILE
    # close ydotool daemon
    if [[ ! -z "${YDOTOOL_PID}" ]]; then
        echo "Closing ydotoold..."
        kill ${YDOTOOL_PID}
    fi
}

ydotoold &
YDOTOOL_PID=$(ps -C ydotoold -o pid h)

COUNT=0
while true; do
    if [[ -f $HANDLER ]]; then
        # Fill in with what you want to be running for the loop
    else
        # Sleep on each loop to avoid CPU exhaustion
        sleep 0.1
    fi
done
