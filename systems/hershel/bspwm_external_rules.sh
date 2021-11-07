#!/usr/bin/env bash
# Handler for various window rules that can't just be based on the window class name
###

set -euo pipefail

centered() {
    local width=$1
    local height=$2
    local x_offset=$(bspc query -m focused -T | jq ".rectangle.x")
    local y_offset=$(bspc query -m focused -T | jq ".rectangle.y")
    local x=$(( (( $(bspc query -m focused -T | jq ".rectangle.width") - $width ) / 2 ) + $x_offset ))
    local y=$(( (( $(bspc query -m focused -T | jq ".rectangle.height") - $height ) / 2 ) + $y_offset ))
    echo "rectangle=${width}x${height}+${x}+${y} state=floating"
}

wid=$1
class=$2
case "$class" in
    "") # NoiseTorch doesn't have a class on launch
        net_wm_name=$(xprop -id "$wid" | awk '/_NET_WM_NAME/ {print $3}')
        if [[ -z "$net_wm_name" ]]; then
            exit 0
        fi
        case $(echo $net_wm_name | sed 's/\"//g') in
            "NoiseTorch") centered 860 680 ;;
        esac
        ;;
esac
