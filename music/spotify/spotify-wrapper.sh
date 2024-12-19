#!/usr/bin/env bash

# This is a wrapper to ensure that `spotify_player` gets launched with a daemon
#   running and already authed.  Spotifyd doesn't handle the new auth flow, so let
#   spotify_player generate the credentials, then just sync them with the daemon

set -euo pipefail

SPOTIFYD_CACHE=$HOME/.cache/spotifyd
SPOTIFY_PLAYER_CACHE=$HOME/.cache/spotify-player/
SPOTIFY_PLAYER=$(which spotify_player)

[[ ! -d "$SPOTIFYD_CACHE" ]] && mkdir -p "$SPOTIFYD_CACHE"
if [[ ! -e "$SPOTIFYD_CACHE/credentials.json" ]]; then
    if [[ ! -e "$SPOTIFY_PLAYER_CACHE/credentials.json" ]]; then
        echo "You haven't authed yet, please go through auth flow to generate the credentials file"
        exec $SPOTIFY_PLAYER
    fi
    ln -s $SPOTIFY_PLAYER_CACHE/credentials.json $SPOTIFYD_CACHE/credentials.json
fi

systemctl --user start spotifyd.service
exec $SPOTIFY_PLAYER "$@"
