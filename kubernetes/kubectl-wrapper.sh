#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying kubectl binary
TARGET_BIN="kubectl"
if [[ "$(which $TARGET_BIN)" != "$(which -a $TARGET_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TARGET_BIN | wc -l)
    BIN=$(which -a $TARGET_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    BIN=$(which $TARGET_BIN)
fi

export KUBECONFIG=${XDG_CONFIG_HOME:-$HOME/.config}/kubernetes/config

exec $BIN "$@"
