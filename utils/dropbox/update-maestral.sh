#!/usr/bin/env bash

set -euo pipefail

VENV=$HOME/.local/maestral

echo "Going to upgrade the maestral pip packages in the virtualenv..."

BEFORE=$($VENV/bin/python -m pip freeze)
$VENV/bin/python -m pip install --upgrade maestral maestral-qt | grep -v "Requirement already satisfied"

[[ "$BEFORE" == "$($VENV/bin/python -m pip freeze)" ]] && exit 1
systemctl --user restart dropbox
