#!/usr/bin/env bash
# Handler for various window rules that can't just be based on the window class name
###

set -euo pipefail

centered() {
    local width=$1
    local height=$2
    local x=$(( ( $(bspc query -m $(bspc query -M) -T | jq ".rectangle.width") - $width ) / 2 ))
    local y=$(( ( $(bspc query -m $(bspc query -M) -T | jq ".rectangle.height") - $height ) / 2))
    echo "rectangle=${width}x${height}+${x}+${y}"
}

wid=$1
class=$2
case "$class" in
    # The file chooser in lutris ends up being *huge*
    lutris)
        case "$(xprop -id "$wid"
          | awk '/WM_WINDOW_ROLE/ {print $3}'
          | sed 's/\"//g')" in
            GtkFileChooserDialog) centered 800 600 ;;
        esac
        ;;
esac
