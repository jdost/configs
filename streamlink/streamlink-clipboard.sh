#!/usr/bin/env bash

set -euo pipefail

msg() {
    if [[ "${TERM:-}" != "linux" ]]; then
        echo "$*"
    else
        notify-send \
            --app-name=streamlink \
            --expire-time=4000 \
            "Streamlink Helper" \
            "$*"
    fi
}

TARGET=$(xclip -out -selection clipboard)
HANDLER="streamlink"

if [[ -z "$TARGET" ]]; then
    msg "Must have a URL to watch in clipboard"
    exit 1
fi

if [[ "$TARGET" =~ .*youtube\.com.* ]]; then
    # For youtube, try to use mpv directly since streamlink will refuse some videos
    HANDLER="mpv"
fi

if ! streamlink --can-handle-url "$TARGET"; then
    msg "Cannot stream: $TARGET"
    exit 2
fi

exec $HANDLER "$TARGET"
