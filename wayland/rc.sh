#!/usr/bin/env bash

set -euo pipefail

for rc in ${XDG_CONFIG_HOME:-$HOME/.config}/wayland/rc.d/*; do
    echo "Sourcing $rc..."
    source $rc
done

systemctl --user restart wayland.target

# vim: ft=bash
