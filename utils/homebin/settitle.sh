#!/usr/bin/env bash

set -euo pipefail

args=$*
title=${1:-$(tty | cut -d/ -f3-)}

if [[ -z "${TMUX:-}" ]]; then
    exec echo -ne "\033]0;$title\007"
elif [[ "${TERM_PROGRAM:-}" == "WezTerm" ]]; then
    exec echo -ne "\x1b]2;$title\x1b\\"
else
    exec tmux rename-window "$title"
fi
