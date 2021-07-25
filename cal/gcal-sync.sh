#!/usr/bin/env bash

set -euo pipefail

VIRTUALENV=$HOME/.local/gcal-sync/bin/python
CONFIG_REPO=$(dirname $(realpath $0))

if [[ ! -e $VIRTUALENV ]]; then
    echo "Please create the virtualenv before running..."
    exit 1
fi

exec $VIRTUALENV $CONFIG_REPO/gcal-sync.py
