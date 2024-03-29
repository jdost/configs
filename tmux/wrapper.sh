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
TMUX_CONF=${XDG_CONFIG_HOME:-$HOME/.config}/tmux/tmux.conf
if [[ ! -f "$TMUX_CONF" ]]; then
    TMUX_CONF=$HOME/.tmux.conf
fi

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
        ! _check $name && rm "$TMUX_TMPDIR/$name"
    fi
    if [[ ! -S "$TMUX_TMPDIR/$name" ]]; then
        _debug "Creating new session: $name..."
        $BIN -f $TMUX_CONF -L $name new-session -s $name -d
    fi
    attach $name
}

attach() {
    local name=${1:-$DEFAULT_TMUX}
    # Check if there is a tmux ssh socket, and it is broken, then replace it with
    # the current ssh socket (often due to a broken session being re-attached to)
    local tmux_auth_sock=$HOME/.ssh/tmux-$name.sock
    if [[ -h "$tmux_auth_sock" ]]; then
        _debug "The old ssh socket is broken, attempt to refresh..."
        [[ ! -z "$SSH_AUTH_SOCK" ]] && ln -sf $SSH_AUTH_SOCK $tmux_auth_sock
    fi

    _debug "Attaching to session: $name..."
    settitle "$name"
    exec $BIN -f $TMUX_CONF -L $name attach -t $name
}

_check() {
    local name=${1:-$DEFAULT_TMUX}
    [[ ! -S "$TMUX_TMPDIR/$name" ]] && return 1
    if ! $BIN -f $TMUX_CONF -L $name has-session -t $name &>/dev/null; then
        return 1
    fi
}


case "${1:-}" in
    "") start "$DEFAULT_TMUX" ;;
    start|new|s)
        shift
        SESSION=${1:-$DEFAULT_TMUX}
        start "$SESSION"
        ;;
    attach|a)
        shift
        SESSION=${1:-$DEFAULT_TMUX}
        if ! _check "$SESSION"; then
            echo "$SESSION is not a valid session."
            exit 1
        fi
        attach "$SESSION"
        ;;
    ls)
        for sock in $TMUX_TMPDIR/*; do
            ! _check $(basename $sock) && rm -rf $sock
        done
        exec ls $TMUX_TMPDIR
        ;;
    "--raw")
        shift
        exec $BIN -f $TMUX_CONF "$@"
        ;;
    *)
        exec $BIN -f $TMUX_CONF "$@" ;;
esac
