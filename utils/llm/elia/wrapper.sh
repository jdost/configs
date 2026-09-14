#!/usr/bin/env bash

set -euo pipefail

# Try to trace back and find the folder the launcher is linked from
LAUNCHER="${BASH_SOURCE[0]}"
while [ -h "${LAUNCHER}" ]; do DIR=$( cd -P "$( dirname "${LAUNCHER}" )" &>/dev/null && pwd )
    LAUNCHER=$(readlink "${LAUNCHER}")
    [[ "${LAUNCHER}" != /* ]] && LAUNCHER="${DIR}/${LAUNCHER}"
done
APP_DIR=$( cd -P "$( dirname "${LAUNCHER}" )" &>/dev/null && pwd )

NAME=elia
IMAGE=local/$NAME:$(sha256sum $APP_DIR/Dockerfile | awk '{ print $1 }')
CONFIG_DIR=${XDG_CONFIG_HOME:-$HOME/.config}/$NAME
LOCAL_DIR=$HOME/.local/$NAME
RUN_DIR=$( pwd )
DOCKER_MOUNT_FLAGS=(
    --volume $LOCAL_DIR:/data
    --volume $APP_DIR/config.toml:/config/config.toml
)

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

msg "Launching..."
exec docker run \
    --rm \
    --interactive \
    --tty \
    --name $NAME \
    --hostname $NAME \
    --env-file $CONFIG_DIR/keys.env \
    "${DOCKER_MOUNT_FLAGS[@]}" \
    $IMAGE \
    "$*"
