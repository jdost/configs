#!/usr/bin/env bash

set -euo pipefail

msg() {
    if [[ "${TERM:-}" != "linux" ]]; then
        echo "$*"
    else
        notify-send \
            --app-name=maim \
            --expire-time=4000 \
            "Screenshot Helper" \
            "$*"
    fi
}

[[ -e "${XDG_CONFIG_HOME:-$HOME/.config}/user-dirs.dirs" ]] && \
    source ${XDG_CONFIG_HOME:-$HOME/.config}/user-dirs.dirs

if ! which rofi &>/dev/null ; then
    msg "Requires rofi!"
    exit 1
fi

NOPTS=3
OPTS="select\0icon\x1fimage-crop\nwindow\0icon\x1fwindow\nscreen\0icon\x1fdisplay\n"

take_screenshot() {
    local dst_dir=${XDG_PICTURES_DIR:-$HOME/pictures}/screenshots
    mkdir -p $dst_dir

    local args=$*
    local output=$dst_dir/$(date +%F-%H:%M:%S).png
    # take screenshot
    maim $args $output
    notify-send \
        --image=$output \
        --app-name=maim \
        --expire-time=4000 \
        "Screenshot taken" \
        "$(basename $output)
Copied to clipboard"
    echo $output | xclip -in -selection clipboard
}

selection=$(
    echo -e $OPTS | \
    rofi \
        -no-config \
        -dmenu \
        -theme screencap \
        -theme-str "listview { columns: $NOPTS; } window { width: $(( $NOPTS*100 )); }"
)
case $selection in
    "select") take_screenshot --select ;;
    "window")
        window=$(xdotool getactivewindow || echo "")
        if [[ -z "$window" ]]; then
            msg "No window currently active to capture..."
            exit 1
        fi
        take_screenshot --window=$window
        ;;
    "screen") take_screenshot ;;
    "") ;;
    *)
        # This shouldn't happen, but handle in case...
        msg "$selection is not a valid option"
        exit 1
        ;;
esac
