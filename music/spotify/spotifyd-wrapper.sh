#!/usr/bin/env bash

set -euo pipefail

HOSTNAME=$(cat /proc/sys/kernel/hostname)

# This is only so we can resolve the cache-path easily without hardcoding users
exec spotifyd \
    --no-daemon \
    --device-name="Daemon - $HOSTNAME" \
    --cache-path=$HOME/.cache/spotifyd/ \
    "$@"
