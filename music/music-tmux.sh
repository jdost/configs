#!/usr/bin/env bash

set -euo pipefail

# This is a multi form launcher, that is just fancy for saying it does both the
#   actual setup of the tmux session, and also handles creating/raising the session
#   if it is not already created/exists elsewhere.  This means that you can run this
#   command and it will resolve to a desired state, but also this is in charge of
#   setting up that state if it doesn't exist.

CLASS="music-sidebar"
PIDFILE="/var/run/user/$UID/$CLASS.pid"
WIDTH=600
VOFFSET=22  # Roughly the heigth of the statusbar

fill_tmux() {
    # Run in a fresh tmux session, this launches the various applications inside of
    #   windows and panes
    which cmus &>/dev/null && tmux new-window -a -n cmus cmus
    which pulsemixer &>/dev/null && tmux new-window -a -n mixer pulsemixer
    tmux select-window -t 1
    settitle ncspot
    # Enable mouse mode, kind of convenient
    tmux set mouse on
    # Hide the status, it is clutter
    tmux set status-left '#[fg=colour39] ﱘ '
    tmux set status-right ''
    exec ncspot
}

bspwm_show_window() {
    # Sets the bspc flags to use the already created window
    bspc node $(cat $PIDFILE) --flag hidden
    bspc node $(cat $PIDFILE) --focus
    return 0
}

bspwm_setup_window() {
    # Skip this if already set
    bspc rule -l | grep "^$CLASS:" &>/dev/null && return 0
    # Sets the bspc rules for the new window to have it be a right-side bar
    local height=$(bspc query -m "primary" -T | jq ".rectangle.height")
    bspc rule -a $CLASS sticky=on state=floating hidden=off rectangle=${WIDTH}x$(( $height - $VOFFSET ))+2000+${VOFFSET}
}

# If this is in a tmux, it means we are using it to set up the session
[[ ! -z "${TMUX:-}" ]] && fill_tmux

# Check if there is a user pid file, then confirm the pid still exists
if [[ -e $PIDFILE ]]; then
    if which bspc &>/dev/null; then
        # if there is an already running process, lets try and show it
        if bspc query --nodes | grep "^$(cat $PIDFILE)$" &>/dev/null; then
            bspwm_show_window && exit 0
        fi
    else
        # TODO add support for other window managers...
        echo "Don't know how to raise a pid in this window manager..."
        exit 1
    fi

    # The corresponding PID doesn't exist, it is a dead file, so clear it
    rm $PIDFILE
fi

if [[ -z "${TERM:-}" || "${TERM:-}" == "linux" ]]; then
    which bspc &>/dev/null && bspwm_setup_window
    exec alacritty --class $CLASS,$CLASS -t music -e "$0"
fi

# store the parent process id, since that is the actual terminal
if [[ -z "${WINDOWID:-}" ]]; then
    echo "Not triggered in a WM..."
    exit 1
fi
echo 0x$(printf '%08x\n' $WINDOWID) > $PIDFILE
# create the tmux session if it doesn't exist, this will run the above setup logic
#   within the session
if ! tmux list-sessions | grep $CLASS; then
    tmux new-session -d -s $CLASS "$0"
fi
# Then attach to it
exec tmux attach-session -t $CLASS
