#!/usr/bin/env bash

set -euo pipefail

TRIGGER=/run/user/${UID}/run-macro

if [[ -f $TRIGGER ]]; then
    exec rm $TRIGGER
else
    sleep 0.5
    exec touch $TRIGGER
fi
