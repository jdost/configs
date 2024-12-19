#!/usr/bin/env bash

set -euo pipefail
# Resolve the wrapped binary
WRAPPED_BIN="playerctl"
if [[ "$(which $WRAPPED_BIN)" != "$(which -a $WRAPPED_BIN | uniq)" ]]; then
   ALIASED_LEN=$(which $WRAPPED_BIN | wc -l)
   BIN=$(which -a $WRAPPED_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
   BIN=$(which $WRAPPED_BIN)
fi

TRACKING_FILE="/run/user/$UID/mpris-tracker"

current_playing() {
    if [[ -e "$TRACKING_FILE" ]]; then
        cat $TRACKING_FILE
        return
    fi

    local players=$(
        $BIN metadata -a --format "{{lc(status)}},{{playerName}}" 2>/dev/null
    )
    if echo $players | grep -e "^playing" &>/dev/null; then
        echo $players | grep -e "^playing" | cut -d',' -f2- | head -n1
    else  # fall back to the first player, which is the default
        echo $players | head -n1 | cut -d',' -f2-
    fi
}

if [[ "${1:-}" == "--current" ]]; then
    shift
    exec $BIN --player=$(current_playing) "$@"
fi

exec $BIN "$@"
