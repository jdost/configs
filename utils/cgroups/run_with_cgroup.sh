#!/usr/bin/env bash

set -euo pipefail

# We use the first argument (the defined executable) to determine the cgroup,
# without it this all fails
if [[ -z "${1:-}" ]]; then
    echo "No provided command to run"
    exit 1
fi

lookup_cgroup() {
    if [[ ! -z "${CGROUP:-}" ]]; then
        echo "${CGROUP}"
        return 0
    fi

    local cmd=$1
    # This is the lookup file for what cgroup to use for $CMD
    local map=${XDG_CONFIG_HOME:-$HOME/.config}/systemd/slice_map
    # Determine the target cgroup/slice
    local slice=""
    if [[ -e "$map" ]]; then
        if grep "^$cmd " $map >&/dev/null; then
            echo $(grep "^$cmd " $map | cut -d' ' -f2)
            return 0
        fi
    fi
    echo ""
}

CMD=$1
SLICE=$(lookup_cgroup $CMD)

# If the computed slice is "none" don't run with systemd-run
if [[ "$SLICE" == "none" ]]; then
    exec "$@"
fi

# Now run the defined command with the determined cgroup
# NOTE: if it's still an empty string, it won't get a cgroup, but will run in an
#   adhoc service scope that you can apply properties to after the launch
exec systemd-run --user --slice=$SLICE "$@"
