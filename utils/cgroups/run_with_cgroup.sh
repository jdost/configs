#!/usr/bin/env bash

set -euo pipefail

# We use the first argument (the defined executable) to determine the cgroup,
# without it this all fails
if [[ -z "${1:-}" ]]; then
    echo "No provided command to run"
    exit 1
fi

CMD=$1
# This is the lookup file for what cgroup to use for $CMD
SLICE_MAP=${XDG_CONFIG_HOME:-$HOME/.config}/systemd/slice_map
# Determine the target cgroup/slice
SLICE=""
if [[ -e "$SLICE_MAP" ]]; then
    if grep "^$CMD" $SLICE_MAP >&/dev/null; then
        SLICE=$(grep "^$CMD" $SLICE_MAP | cut -d' ' -f2)
    else
        echo "$CMD" >> $HOME/tmp/cgroups.log
    fi
fi
# Now run the defined command with the determined cgroup
# NOTE: if it's still an empty string, it won't get a cgroup, but will run in an
#   adhoc service scope that you can apply properties to after the launch
exec systemd-run --user --slice=$SLICE "$@"
