#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying git binary
if [[ "$(which git)" != "$(which -a git | uniq)" ]]; then
   ALIASED_GIT_LEN=$(which git | wc -l)
   GIT_BIN=$(which -a git | uniq | sed -e "1,$ALIASED_GIT_LEN"d | head -n 1)
else
   GIT_BIN=$(which git)
fi

ncurses() {
    local lazygit_path="$HOME/.local/bin/lazygit"
    if [[ ! -x "$lazygit_path" ]]; then
        # prepare the download URL
        local version=$(curl -L -s -H 'Accept: application/json' https://github.com/jesseduffield/lazygit/releases/latest | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/')
        local github_file="lazygit_${version//v/}_$(uname -s)_x86_64.tar.gz"
        local url="https://github.com/jesseduffield/lazygit/releases/download/${version}/${github_file}"

        # install/update the local binary
        curl -L -o lazygit.tar.gz $url
        tar xzvf lazygit.tar.gz lazygit
        mv -f lazygit ${lazygit_path}
        rm lazygit.tar.gz
    fi
    exec $lazygit_path
}

case "${1:-}" in
   "")
      #exec $GIT_BIN
      ncurses
      ;;
   "grep")
      if which rg &>/dev/null; then
         TOPLEVEL=""
         if $GIT_BIN rev-parse --show-toplevel &>/dev/null; then
            TOPLEVEL=$($GIT_BIN rev-parse --show-toplevel 2>/dev/null)
         else
            echo "fatal: not a git repository"
            exit 1
         fi
         shift # Remove the `grep` argument
         exec rg --ignore-file=$TOPLEVEL/.gitignore "$@"
      else
         exec $GIT_BIN "$@"
      fi
      ;;
   "--raw") # Provide a bypass, this will skip the overrides above
      shift
      exec $GIT_BIN "$@"
      ;;
   *)
      exec $GIT_BIN "$@"
      ;;
esac
