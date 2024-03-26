#!/usr/bin/env bash

# TODO
#  - generate notification when paused, button to trigger script

set -euo pipefail

STATEFILE="/var/run/user/$UID/deadd-paused"

pause() {
    touch "$STATEFILE"
    exec notify-send \
        --hint=int:deadd-notification-center:1 \
        --hint=string:type:pausePopups \
        "Pausing Popops..."
}

unpause() {
    rm "$STATEFILE"
    exec notify-send \
        --hint=int:deadd-notification-center:1 \
        --hint=string:type:unpausePopups \
        "Showing Popops..."
}

reset() {
    [[ -e "$STATEFILE" ]] && rm "$STATEFILE"
}

toggle() {
    if [[ -e "$STATEFILE" ]]; then
        unpause
    else
        pause
    fi
}

show() {
    if [[ -e "$STATEFILE" ]]; then
        echo "Paused"
    else
        echo "Showing"
    fi
}


case "${1:-}" in
    "pause"|"p") pause ;;
    "unpause"|"show") unpause ;;
    "toggle"|"t") toggle ;;
    "query"|"state") show ;;
    "reset") reset ;;
    "")
        if [[ "${TERM:-}" == "linux" ]]; then
            toggle
        else
            show
        fi
        ;;
esac
