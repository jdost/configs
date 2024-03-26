#!/usr/bin/env bash

set -euo pipefail

if [[ "$#" == "0" ]]; then
    cat <<-EOF
retry [limit] <COMMAND>

Will retry running COMMAND until successful, (if set) will be limited to a number of
retries before exitting.
EOF
    exit 1
fi

# We say the retry loop is infinite, but just make it really large
LIMIT=99999999
VERBOSE=/bin/true
while [[ "$#" != 0 ]]; do
    case "$1" in
        "--quiet")
            VERBOSE=/bin/false
            shift
            ;;
        [!0-9]*) # If the first argument is not a number, skip
            break
            ;;
        *) # This means it is a number, so pop the value off in place of the default
            LIMIT="$1"
            shift
            ;;
    esac
done
RUN_COUNT=0
EXIT_CODE=-1
while (( $RUN_COUNT < $LIMIT )); do
    if "$@" ; then
        exit 0
    fi
    EXIT_CODE=$?  # Capture the exit code, so we can surface it on the final retry
    (( RUN_COUNT=$RUN_COUNT+1 ))
    if $VERBOSE; then
        echo "Retry #$RUN_COUNT/$LIMIT Failed: $EXIT_CODE..."
    fi
done

exit $EXIT_CODE
