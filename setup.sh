#!/usr/bin/env bash

### THIS IS A TEMP FILE, REPLACE ASAP

set -euo pipefail

show_help() {
  cat <<-HELP
Setup script for bspwm window manager

USAGE: ${0} [command]

commands:
  init   -- Initialize system with expected packages and configs
  link   -- Creates missing links not already defined
HELP
}

linkIfNot() {
  [[ -e "$2" ]] && return

  if [[ ! -d "$(dirname $2)" ]]; then
    echo "Creating missing directory: $(dirname $2)"
    mkdir -p "$(dirname $2)"
  fi

  echo "Linking " $1
  ln -s $PWD/$1 $2
}

link() {
  linkIfNot bspwm/bspwmrc $XDG_CONFIG_HOME/bspwm/bspwmrc
  linkIfNot sxhkd/sxhkdrc $XDG_CONFIG_HOME/sxhkd/sxhkdrc
}

install() {
  sudo pacman -Sy --needed \
    bspwm \
    sxhkd
}

case "${1:-}" in
  'init')
    install
    link
    ;;
  'link')
    link
    ;;
esac
