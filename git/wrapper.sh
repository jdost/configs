#!/usr/bin/env bash

set -euo pipefail
# Resolve the underlying git binary
if [[ "$(which git)" != "$(which -a git | uniq)" ]]; then
   ALIASED_GIT_LEN=$(which git | wc -l)
   GIT_BIN=$(which -a git | uniq | sed -e "1,$ALIASED_GIT_LEN"d | head -n 1)
else
   GIT_BIN=$(which git)
fi

case "${1:-}" in
   "")
      exec $GIT_BIN
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
