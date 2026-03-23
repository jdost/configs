#!/usr/bin/env bash

set -euo pipefail

# Try to trace back and find the folder the launcher is linked from
LAUNCHER="${BASH_SOURCE[0]}"
while [ -h "${LAUNCHER}" ]; do DIR=$( cd -P "$( dirname "${LAUNCHER}" )" &>/dev/null && pwd )
    LAUNCHER=$(readlink "${LAUNCHER}")
    [[ "${LAUNCHER}" != /* ]] && LAUNCHER="${DIR}/${LAUNCHER}"
done
APP_DIR=$( cd -P "$( dirname "${LAUNCHER}" )" &>/dev/null && pwd )

NAME=claude
IMAGE=local/$NAME:$(sha256sum $APP_DIR/Dockerfile | awk '{ print $1 }')
CONFIG_DIR=${XDG_CONFIG_HOME:-$HOME/.config}/$NAME
DEFAULT_CONFIG_DIR=$CONFIG_DIR/.claude

if RUN_DIR=$(git rev-parse --show-toplevel 2>/dev/null); then
  cd "$RUN_DIR"
else
  echo "Not inside a git repository" >&2
  RUN_DIR=$( pwd )
fi

msg() {
    echo "$*"
}

build() {
    msg "Building a new container image..."
    # Determine CPU architecture
    ARCH=""
    case $(uname -m) in
        aarch64|arm64)
            ARCH=arm64 ;;
        x86_64|amd64)
            ARCH=x64 ;;
        *)
            echo "Unhandled CPU architecture: $(uname -m)"
            exit 1 ;;
    esac

    GID=$(id -g)
    export DOCKER_BUILDKIT=1
    cd $APP_DIR
    if ! docker build \
        --force-rm \
        --build-arg UID=${UID} \
        --build-arg GID=${GID} \
        --build-arg ARCHITECTURE=${ARCH} \
        --tag "${IMAGE}" . ; then
        msg "Image build failed"
        exit 1
    fi
    cd $RUN_DIR
}

# There is no image for this current tag, based on the Dockerfile checksum
if [[ -z "$(docker images --quiet $IMAGE)" ]]; then
    build
fi

PARSED_ARGS=""
MODE="r"
while [[ $# -gt 0 ]]; do
  case $1 in
      --read-only|--read|-r)
          MODE="r"
          shift
          ;;
      --write|-w)
          MODE="w"
          shift
          ;;
      *)
          if [[ -z "${PARSED_ARGS}" ]]; then
              PARSED_ARGS="${1}"
          else
              PARSED_ARGS="${PARSED_ARGS} ${1}"
          fi
          shift
          ;;
  esac
done

# If run with the read-only flag, mount all files as read-only
MOUNT_SUFFIX=""
if [[ "${MODE}" == "r" ]]; then
    MOUNT_SUFFIX=":ro"
fi
if [[ -d $CONFIG_DIR ]]; then
    # Because the skills folder is a symlink to the configs, we just mount it
    # directly from here
    DOCKER_MOUNT_FLAGS=(
        --env CLAUDE_CONFIG_DIR=/home/claude/.config/claude
        --volume $CONFIG_DIR:/config/xdg_claude
        --volume $APP_DIR/skills:/config/xdg_claude/skills$MOUNT_SUFFIX
        --volume $DEFAULT_CONFIG_DIR:/config/claude
    )
fi

msg "Launching..."
exec docker run \
    --rm \
    --interactive \
    --tty \
    --name $NAME \
    "${DOCKER_MOUNT_FLAGS[@]}" \
    --volume ${RUN_DIR}:/code$MOUNT_SUFFIX \
    $IMAGE \
    /usr/local/bin/claude "$PARSED_ARGS"
