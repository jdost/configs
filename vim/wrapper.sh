#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying binary
TGT_BIN="vim"
if [[ "$(which $TGT_BIN)" != "$(which -a $TGT_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TGT_BIN | wc -l)
    _BIN=$(which -a $TGT_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    _BIN=$(which $TGT_BIN)
fi

export VIMINIT='let $MYVIMRC="$HOME/.config/vim/vimrc" | source $MYVIMRC'
# Unsure why, but having alacritty as the terminal messes up ctrlp's arrow keys
if [[ "$TERM" == "alacritty" ]]; then
    export TERM="screen-256color"
fi
exec $_BIN "$@"
