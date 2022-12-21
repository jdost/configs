FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libx11-xcb1 \
        libgbm1 \
        libasound2 \
        libdrm2 \
    && echo "deb [trusted=yes] https://apt.fury.io/notion-repackaged/ /" \
        > /etc/apt/sources.list.d/notion.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        notion-app \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# Because we use volume mounting, we want to keep the runtime UID and GID the same
#   as on the host
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID notion \
    && useradd -d /home/notion -s /bin/bash -m notion -u $UID -g $GID \
    && mkdir -p /home/notion/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/notion/.config/gtk-3.0/settings.ini \
    && chown -R $UID:$GID /home/notion/.config \
    && mkdir -p /config && chown -R $UID:$GID /config \
    && ln -s /config /home/notion/.config/notion-app

USER notion
# --no-sandbox runs it without containment, we are achieving this by running it in
#   a docker container
# --disable-dev-shm-usage fixes an issue with the shared memory being too small when
#   run via a docker container
CMD [ "notion-app", "--no-sandbox", "--disable-dev-shm-usage" ]
