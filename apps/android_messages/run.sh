#!/usr/bin/env bash

set -euo pipefail

# Try to trace back and find the folder the launcher is linked from
LAUNCHER="${BASH_SOURCE[0]}"
while [ -h "$LAUNCHER" ]; do DIR=$( cd -P "$( dirname "$LAUNCHER" )" &>/dev/null && pwd )
    LAUNCHER=$(readlink $LAUNCHER)
    [[ "$LAUNCHER" != /* ]] && LAUNCHER="$DIR/$LAUNCHER"
done
APP_DIR=$( cd -P "$( dirname "$LAUNCHER" )" &>/dev/null && pwd )
RUN_DIR=$( pwd )

NAME=android-messages
IMAGE_TAG=$(sha256sum $APP_DIR/Dockerfile | awk '{ print substr($1, 0, 24) }')
IMAGE=desktop-app/$NAME:$IMAGE_TAG
CONFIG_DIR=${XDG_CONFIG_HOME:-$HOME/.config}/$NAME
DOCKER_FLAGS_X=(
    --hostname $(cat /proc/sys/kernel/hostname)
    --env DISPLAY=$DISPLAY
    --volume $HOME/.Xauthority:/tmp/.Xauthority:ro
    --env XAUTHORITY=/tmp/.Xauthority
    --volume /tmp/.X11-unix:/tmp/.X11-unix:ro
)
DOCKER_FLAGS_DBUS=(
    --env DBUS_SESSION_BUS_ADDRESS=unix:path=/var/run/user/$UID/bus
    --volume /etc/localtime:/etc/localtime:ro
    --volume /etc/machine-id:/etc/machine-id:ro
    --volume /var/run/user/$UID:/var/run/user/$UID
)


msg() {
    if [[ "${TERM:-}" != "linux" ]]; then
        echo "$*"
    else
        notify-send \
            --app-name=$NAME \
            --expire-time=4000 \
            "Docker App: $NAME" \
            "$*"
    fi
}

build() {
    msg "Building a new container image..."
    GID=$(id -g)
    cd $APP_DIR
    export DOCKER_BUILDKIT=1
    if ! docker build \
        --force-rm \
        --build-arg UID=$UID \
        --build-arg GID=$GID \
        --tag "$IMAGE" . ; then
        msg "Image build failed"
        exit 1
    fi
    cd $RUN_DIR
}

# There is no image for this current tag, based on the Dockerfile checksum
if [[ -z "$(docker images --quiet $IMAGE)" ]]; then
    build
fi

[[ ! -d "$CONFIG_DIR" ]] && mkdir "$CONFIG_DIR"

exec docker run \
    --rm \
    --interactive \
    --name $NAME \
    --volume $CONFIG_DIR:/config \
    "${DOCKER_FLAGS_X[@]}" \
    "${DOCKER_FLAGS_DBUS[@]}" \
    $IMAGE
