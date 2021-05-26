#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying binary
TGT_BIN="vim"
if [[ "$(which $TGT_BIN)" != "$(which -a $TGT_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TGT_BIN | wc -l)
    BIN=$(which -a $TGT_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    BIN=$(which $TGT_BIN)
fi

VIMRC=${XDG_CONFIG_HOME:-$HOME/.config}/vim/vimrc
# Need to guard this in case `vim` is run with `sudo`
if [[ -e "$VIMRC" ]]; then
    export VIMINIT="let \$MYVIMRC=\"$VIMRC\" | source \$MYVIMRC"
fi

# Unsure why, but having alacritty as the terminal messes up ctrlp's arrow keys
if [[ "$TERM" == "alacritty" ]]; then
    export TERM="screen-256color"
fi
exec $BIN "$@"
