#!/usr/bin/env bash

set -euo pipefail

side=${1:-"right"}
CLASS="sidebar.$side"


setup_window() {
    local current_workspace_info=$(hyprctl monitors -j | jq ".[] | select(.focused)")
    local target_height=$(echo $current_workspace_info | jq ".height")
    local target_width=$(echo $current_workspace_info | jq ".width")

    #hyprctl dispatch resizewindowpixel exact \
    #    $(( $target_width / 3 )) \
    #    $(( $target_height - 4 )),class:$CLASS

    if [[ "$side" == "right" ]]; then
        hyprctl dispatch movewindowpixel exact \
            $(( $target_width * 2 / 3 - 2)) 2,class:$CLASS
    else
        hyprctl dispatch movewindowpixel \
            exact 0 2,class:$CLASS
    fi
}

if ! hyprctl clients | grep "initialClass: $CLASS" &>/dev/null; then
    x="0"
    if [[ "$side" == "right" ]]; then
        x="66%"
    fi
    # there is not an existing window, so spawn it
    hyprctl dispatch exec "[move $x 0] wezterm --config window_background_opacity=0.4 start --cwd $HOME --class \"$CLASS\""
    sleep 0.08
    setup_window
    exit 0
fi

loc=$(
    hyprctl clients -j | \
    jq ".[] | select(.class == \"$CLASS\").workspace.id"
)
current_workspace=$(hyprctl activeworkspace -j | jq ".id")

if [[ "$loc" == "$current_workspace" ]]; then
    if [[ $(hyprctl activewindow -j | jq -r ".class") != $CLASS ]]; then
        hyprctl dispatch focuswindow class:$CLASS
    else
        # window is currently on the active workspace, so hide it by sending it to a
        #   special workspace
        hyprctl --batch "dispatch togglespecialworkspace sidebars ;
            dispatch movetoworkspace special:sidebars,class:$CLASS ;
            dispatch togglespecialworkspace sidebars ;
            dispatch cyclenext"
    fi
else
    # window is located on another workspace, bring it to this one
    hyprctl dispatch movetoworkspace $current_workspace,"class:$CLASS"
    setup_window
fi
