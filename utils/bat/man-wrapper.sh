#!/usr/bin/env bash

# Man wrapper to use `bat` for better output and paging

set -euo pipefail
# Resolve the underlying man binary
TARGET_BIN="man"
if [[ "$(which $TARGET_BIN)" != "$(which -a $TARGET_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TARGET_BIN | wc -l)
    BIN=$(which -a $TARGET_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    BIN=$(which $TARGET_BIN)
fi

export MANROFFOPT="-c"
export MANPAGER="sh -c 'col -bx | bat -l man --paging auto --plain'"

exec $BIN "$@"
