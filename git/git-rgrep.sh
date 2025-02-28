#!/usr/bin/env bash

set -euo pipefail

if ! command -v rg &>/dev/null; then
    echo "This required 'rg' to be installed and on the PATH..."
    exit 1
fi

TOPLEVEL=""
if git rev-parse --show-toplevel &>/dev/null; then
    TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
else
    echo "fatal: not a git repository"
    exit 1
fi

rg \
    --ignore-file=$TOPLEVEL/.gitignore \
    --column \
    --line-number \
    --no-heading \
    --color=always \
    --smart-case \
    --json \
    "$@" \
| delta
