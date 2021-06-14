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

if [[ -z "$TARGET" ]]; then
    msg "Must have a URL to watch in clipboard"
    exit 1
fi

if ! streamlink --can-handle-url "$TARGET"; then
    msg "Cannot stream: $TARGET"
    exit 2
fi

exec streamlink "$TARGET"
