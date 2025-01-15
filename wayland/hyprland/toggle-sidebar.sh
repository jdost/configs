#!/usr/bin/env bash

set -euo pipefail

side=${1:-"right"}
CLASS="sidebar.$side"


if ! hyprctl clients | grep "initialClass: $CLASS" &>/dev/null; then
    x="0"
    if [[ "$side" == "right" ]]; then
        x="66%"
    fi
    # there is not an existing window, so spawn it
    exec hyprctl dispatch exec "[move $x 0] wezterm --config window_background_opacity=0.4 start --cwd $HOME --class \"$CLASS\""
fi

loc=$(
    hyprctl clients -j | \
    jq ".[] | select(.class == \"$CLASS\").workspace.id"
)
current_workspace=$(hyprctl activeworkspace -j | jq ".id")

if [[ "$loc" == "$current_workspace" ]]; then
    # window is currently on the active workspace, so hide it by sending it to a
    #   special workspace
    hyprctl --batch "dispatch togglespecialworkspace sidebars ;
        dispatch movetoworkspace special:sidebars,class:$CLASS ;
        dispatch togglespecialworkspace sidebars ;
        dispatch cyclenext"
else
    # window is located on another workspace, bring it to this one
    hyprctl dispatch movetoworkspace $current_workspace,"class:$CLASS"
    if [[ "$side" == "right" ]]; then
        hyprctl dispatch movewindow r
    else
        hyprctl dispatch movewindow l
    fi
fi
