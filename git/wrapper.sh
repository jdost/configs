#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying git binary
TARGET_BIN="git"
if [[ "$(which $TARGET_BIN)" != "$(which -a $TARGET_BIN | uniq)" ]]; then
    ALIASED_LEN=$(which $TARGET_BIN | wc -l)
    BIN=$(which -a $TARGET_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
    BIN=$(which $TARGET_BIN)
fi

ncurses() {
    local lazygit_path="$HOME/.local/bin/lazygit"
    if [[ ! -x "$lazygit_path" ]]; then
        # prepare the download URL
        local version=$(curl -L -s -H 'Accept: application/json' https://github.com/jesseduffield/lazygit/releases/latest | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/')
        local github_file="lazygit_${version//v/}_$(uname -s)_x86_64.tar.gz"
        local url="https://github.com/jesseduffield/lazygit/releases/download/${version}/${github_file}"

        # install/update the local binary
        curl -sL -o lazygit.tar.gz $url
        tar xzf lazygit.tar.gz lazygit
        mv -f lazygit ${lazygit_path}
        rm lazygit.tar.gz
    fi
    exec $lazygit_path
}

case "${1:-}" in
    "")
        #exec $BIN
        ncurses
        ;;
    "grep")
        if which rg &>/dev/null; then
            shift
            exec git-rgrep "$@"
        else
            exec $BIN "$@"
        fi
        ;;
    "--raw") # Provide a bypass, this will skip the overrides above
        shift
        exec $BIN "$@"
        ;;
    *)
        exec $BIN "$@"
        ;;
esac
