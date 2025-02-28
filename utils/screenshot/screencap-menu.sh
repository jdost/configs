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

if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]] then
    export IS_WAYLAND=/bin/false
else
    export IS_WAYLAND=/bin/true
fi

take_screenshot() {
    local dst_dir=${XDG_PICTURES_DIR:-$HOME/pictures}/screenshots
    mkdir -p $dst_dir

    local target=${1:-screen}
    local output=$dst_dir/$(date +%F-%H:%M:%S).png
    # take screenshot
    if $IS_WAYLAND; then # this is really IS_HYPRLAND >.>
        if [[ "$target" == "select" ]]; then
            slurp | grim -g - $output
        elif [[ "$target" == "window" ]]; then
            hyprctl -j activewindow | jq -r '"\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"' | grim -g - $output
        else  # "screen"
            hyprctl -j activeworkspace | jq -r '.monitor' | grim -o - $output
        fi
    else
        if [[ "$target" == "select" ]]; then
            maim --select $output
        elif [[ "$target" == "window" ]]; then
            window=$(xdotool getactivewindow || echo "")
            if [[ -z "$window" ]]; then
                msg "No window currently active to capture..."
                exit 1
            fi
            maim --window=$window $output
        else  # "screen"
            main $output
        fi
    fi

    populate_clipboard() {
        if $IS_WAYLAND; then
            cat $output | wl-copy
        else
            echo $output | xclip -in -selection clipboard
        fi
    }

    populate_clipboard

    notify-send \
        --app-name=screenshot \
        --icon=$output \
        --expire-time=4000 \
        --transient \
        "Screenshot taken" \
        "$(basename $output) Copied to clipboard"
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
    "select") take_screenshot "select" ;;
    "window") take_screenshot "window" ;;
    "screen") take_screenshot "screen" ;;
    "") ;;
    *)
        # This shouldn't happen, but handle in case...
        msg "$selection is not a valid option"
        exit 1
        ;;
esac
