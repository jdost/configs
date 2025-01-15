#!/usr/bin/env bash

set -euo pipefail

interactive=/bin/true
PROMPT_TIMEOUT=5000

# Handle the various circumstances for this being called
if [[ "${CLIPBOARD_STATE:-}" == "data" ]]; then
    # If called with this set, it means it was launched from `wl-paste --watch`, so
    #   we pull the target from stdin, print issues to stdout (for logs) and treat
    #   this as non-manually launched (so prompt for interruptive actions)
    target=$(cat)
    msg() { echo "$*"; }
    interactive=/bin/false
elif [[ ! -z "${CLIPBOARD_STATE:-}" ]]; then
    # This was called by `wl-paste --watch` but is passing non data on the clipboard
    exit 0
else
    # This was launched manually, so we pull the target from the paste buffer and
    #   raise messages to the user via notifications to give them visibility on
    #   issues
    if which wl-paste &>/dev/null; then
        target=$(wl-paste)
    else
        target=$(xclip -out -selection clipboard)
    fi
    msg() {
        notify-send --app-name=streamlink --expire-time=3000 "Clipboard Video Helper" "$*";
    }
fi

if [[ -z "$target" ]]; then
    msg "Must have contents on the clipboard to watch..."
    exit 1
fi

handler=$(web-xdg-open --lookup $target)
cmd=$(echo $handler | awk '{ print $1 }')
if [[ "$cmd" == "mpv" || "$cmd" == "streamlink" ]]; then
    echo "Notification prompt to use '$cmd' for '$target'"
else  # Probably a browser handled URL, do nothing
    exit 0
fi

# Check with streamlink if the match (for some reason) doesn't work
if [[ "$handler" == "streamlink" ]]; then
    if ! streamlink --can-handle-url "$target"; then
        msg "Cannot stream: $target"
        exit 2
    fi
fi


if $interactive; then
    exec $handler
else
    # Launch the notification as a background process so the notification doesn't
    #   block subsequent clipboard events while it's waiting for potential
    #   interactions
    (
        icon=$cmd
        if [[ "$icon" == "streamlink" ]]; then
            icon="gnome-twitch"
        fi
        sleep 0
        notify-send \
            --app-name=$cmd \
            --icon=$icon \
            --transient \
            --action=launch=Open \
            --wait \
            --expire-time=$PROMPT_TIMEOUT \
            "Open with $cmd" \
            "Use \`$cmd\` to watch $target" \
        | while read -r action; do
            if [[ "$action" == "launch" ]]; then
                exec $handler
            else
                msg "Unknown action: $action"
                exit 1
            fi
        done
    ) &
fi
