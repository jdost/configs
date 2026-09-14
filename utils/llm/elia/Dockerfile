FROM ubuntu:24.04

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update \
    && apt-get install --no-install-recommends -y \
        pipx \
    && userdel ubuntu \
    && rm -rf /var/lib/apt/lists/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID elia \
    && useradd -d /home/elia -s /bin/bash -m elia -u $UID -g $GID \
    && mkdir -p /home/elia/.config && chown -R $UID:$GID /home/elia/.config \
    && mkdir -p /config && chown -R $UID:$GID /config \
    && ln -s /config /home/elia/.config/elia \
    && mkdir -p /home/elia/.local/share && chown -R $UID:$GID /home/elia/.local \
    && mkdir -p /data && chown -R $UID:$GID /data \
    && ln -s /data /home/elia/.local/share/elia

USER elia

RUN pipx install elia-chat

ENTRYPOINT ["/home/elia/.local/bin/elia"]
