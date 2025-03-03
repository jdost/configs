#!/usr/bin/env bash

set -euo pipefail

WORKSPACES_PER_MONITOR=5

if [[ "$#" -lt 2 ]]; then
    echo "Not enough arguments..."
    exit 1
fi

focused_monitor=$(hyprctl activeworkspace -j | jq ".monitorID")
target_workspace=$(( $focused_monitor * $WORKSPACES_PER_MONITOR + $2 ))

case "$1" in
    "switch")
        hyprctl dispatch workspace $target_workspace
        ;;
    "move")
        hyprctl dispatch movetoworkspace $target_workspace
        ;;
    *)
        echo "Unknown action: $1"
        exit 1
esac
