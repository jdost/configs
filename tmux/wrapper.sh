#!/usr/bin/env bash

set -euo pipefail
# If there is more than one `tmux` result in the path, we need to figure out the
#  precedence and target the proper binary.  This is mainly due to something like
#  this script or a shell alias existing above the actual binary
TARGET_BIN="tmux"
if [[ "$(which $TARGET_BIN)" != "$(which -a $TARGET_BIN)" ]]; then
   ALIASED_LEN=$(which $TARGET_BIN | wc -l)
   BIN=$(which -a $TARGET_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
   BIN=$(which $TARGET_BIN)
fi

# Set up some defaults
TMUX_TMPDIR=/tmp/tmux-$UID
DEFAULT_TMUX=default

if [[ ! -d "$TMUX_TMPDIR" ]]; then
    mkdir -p "$TMUX_TMPDIR"
    chmod 700 "$TMUX_TMPDIR"
fi

_debug() {
    [[ -z "${DEBUG:-}" ]] && return
    echo " >>> $*"
}

start() {
    local name=${1:-$DEFAULT_TMUX}
    _debug "Starting $name..."
    if [[ -S "$TMUX_TMPDIR/$name" ]]; then
        if ! $BIN has-session -t $name &>/dev/null; then
            _debug "Removing unused session $name..."
            rm "$TMUX_TMPDIR/$name"
        fi
    fi
    if [[ ! -S "$TMUX_TMPDIR/$name" ]]; then
        _debug "Creating new session: $name..."
        $BIN -L $name new-session -s $name -d
    fi
    attach $name
}

attach() {
    local name=${1:-$DEFAULT_TMUX}
    _debug "Attaching to session: $name..."
    settitle "$name"
    exec $BIN -L $name attach -t $name
}

_check() {
    if [[ -z "${TMUX:-}" ]]; then
        echo "!!! Not currently in a tmux session"
        exit 1
    fi
}


case "${1:-}" in
    "") start "$DEFAULT_TMUX" ;;
    start|new|s)
        shift
        start "${1:-$DEFAULT_TMUX}"
        ;;
    attach|a)
        shift
        attach "${1:-$DEFAULT_TMUX}"
        ;;
    ls) exec ls $TMUX_TMPDIR ;;
    "--raw")
        shift
        exec $BIN "$@"
        ;;
    *)
        exec $BIN "$@" ;;
esac
