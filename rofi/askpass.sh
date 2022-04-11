#!/usr/bin/env bash

set -euo pipefail

exec rofi -dmenu \
    -password \
    -mesg "$*" \
    -theme askpass
