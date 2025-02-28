#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying binary
TGT_BIN=$(basename "$0")
if [[ "$(which $TGT_BIN)" != "$(which -a $TGT_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TGT_BIN | wc -l)
    BIN=$(which -a $TGT_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    BIN=$(which $TGT_BIN)
fi

export WGETRC=${XDG_CONFIG_DIR:-$HOME/.config}/wgetrc

exec $BIN "$@"
