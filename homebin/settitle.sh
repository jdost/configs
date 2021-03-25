#!/usr/bin/env bash

set -euo pipefail

args=$*
title=${1:-$(tty | cut -d/ -f3-)}

if [[ -z "${TMUX:-}" ]]; then
   exec echo -ne "\033]0;$title\007"
else
   exec printf "\033k$title\033\\"
fi
