#!/usr/bin/env bash

set -euo pipefail

BOLD="\033[1m";     UNDERLINE="\033[4m";    RESET="\033[0m"
BLACK="\033[30m";   RED="\033[31m";         GREEN="\033[32m"
BROWN="\033[33m";   BLUE="\033[34m";        PURPLE="\033[35m"
CYAN="\033[36m";    LGREY="\033[37m"

# Text Effects
bold() { echo -en "${BOLD}$*${RESET}"; }
underline() { echo -en "${UNDERLINE}$*${RESET}"; }

# Colors
black() { echo -en "${BLACK}$*${RESET}"; }
dark_grey() { bold $(black $*); }
red() { echo -en "${RED}$*${RESET}"; }
pink() { bold $(red $*); }
green() { echo -en "${GREEN}$*${RESET}"; }
light_green() { bold $(green $*); }
brown() { echo -en "${BROWN}$*${RESET}"; }
yellow() { bold $(brown $*); }
blue() { echo -en "${BLUE}$*${RESET}"; }
light_blue() { bold $(blue $*); }
purple() { echo -en "${PURPLE}$*${RESET}"; }
magenta() { bold $(purple $*); }
cyan() { echo -en "${CYAN}$*${RESET}"; }
light_cyan() { bold $(cyan $*); }
light_grey() { echo -en "${LGREY}$*${RESET}"; }
white() { bold $(light_grey $*); }

time_alias() { sed 's# week\(s*\),#w#; s# day\(s*\),#d#; s# hour\(s*\),#h#; s# minute\(s*\)#m#'; }
# General Information
echo ''
#  User: $USER   Host: $HOST   Directory: $PWD
echo -en "  $(light_green 'User:') $(blue $USER)"
echo -en "\t$(light_green 'Host:') $(blue $(cat /proc/sys/kernel/hostname))"
echo -en "\t$(light_green 'Directory:') $(blue $(echo $PWD | sed "s#$HOME#\~#"))"
echo ''
#   TTY: $TTY   Jobs: #JOBS    Shell: $SHELL
echo -en "    $(light_green 'TTY:') $(blue $(tty | cut -d'/' -f3-))"
echo -en "\t$(light_green 'Jobs:') $(blue $(ps T | awk '{ if($3 == "T"){ print } }' | wc -l))  "
echo -en "\t$(light_green 'Shell:') $(blue $SHELL)"
echo ''
#   Time: HH:MM:SS  Uptime: 5d 4h 3m
echo -en "    $(light_green 'Time:') $(blue $(date +'%b %d %R'))"
echo -en "\t\t$(light_green 'Uptime:') $(blue $(uptime -p | cut -d' ' -f2- | time_alias))"
echo ''
#    Kernel: ...
echo -en "    $(light_green 'Kernel:') $(blue $(uname -srmo))"
echo ''

# Language/tool runtimes
if which python &>/dev/null; then
    echo -en "   $(pink 'Python:') $(light_grey $(python --version 2>&1 | cut -d' ' -f2-))"
else
    echo -en "   $(pink 'Python:') $(light_grey 'uninstalled')"
fi
if which docker &>/dev/null; then
    echo -en "\t\t$(pink 'Docker:') $(light_grey $(docker --version | cut -d' ' -f3 | cut -d',' -f1))"
else
    echo -en "\t\t$(pink 'Docker:') $(light_grey 'uninstalled')"
fi
echo ''

HAS_OPT=0
secho() {
    if [[ $HAS_OPT ]]; then
        echo ''
        HAS_OPT=1
    fi
    echo -e "$*"
}
# Local runtime
if [[ ! -z "${VIRTUAL_ENV:-}" ]]; then
    secho "  $(brown 'Virtual Environment:') $(white $(basename ${VIRTUAL_ENV}))"
fi
if [[ ! -z "${SSH_CONNECTION:-}" ]]; then
    ssh_client=$(echo $SSH_CONNECTION | cut -d' ' -f1-2 --output-delimiter=':')
    ssh_host=$(echo $SSH_CONNECTION | cut -d' ' -f3-4 --output-delimiter=':')
    secho "  $(brown 'SSH:') $(white $ssh_client)$(yellow '->')$(white $ssh_host)"
fi
if [[ ! -z "${TMUX:-}" ]]; then
    tmux_name=$(echo $TMUX | cut -d',' -f1 | rev | cut -d'/' -f1 | rev)
    tmux_info="$(tmux list-panes | wc -l) panes / $(tmux list-windows | wc -l) windows"
    secho "  $(brown 'Tmux:') $(white $tmux_name) - $(white $tmux_info)"
fi

echo ''
