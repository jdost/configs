#!/usr/bin/env bash

set -euo pipefail

args=$*
if [[ -z "${SSH_CLIENT:-}" ]]; then
    default_title=$(tty | cut -d/ -f3-)
else
    default_title="$(cat /proc/sys/kernel/hostname):$(tty | cut -d/ -f3-)"
fi
title=${1:-$default_title}

if [[ -z "${TMUX:-}" ]]; then
    exec echo -ne "\033]0;$title\007"
elif [[ "${TERM_PROGRAM:-}" == "WezTerm" ]]; then
    exec echo -ne "\x1b]2;$title\x1b\\"
else
    exec tmux rename-window "$title"
fi
