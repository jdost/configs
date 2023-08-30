FROM ubuntu:20.04

# The installer is sourced from the project's github release page, so we can define
#   the target version via an arg
ARG VERSION=5.4.1
ARG DEB_RELEASE_URI=https://github.com/OrangeDrangon/android-messages-desktop/releases/download

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libasound2 \
        libdrm2 \
        libgbm1 \
        libx11-xcb1 \
        wget \
        xclip \
    && wget --quiet -O /tmp/android-messages.deb $DEB_RELEASE_URI/v${VERSION}/Android.Messages-v${VERSION}-linux-amd64.deb \
    && apt install -y --no-install-recommends /tmp/android-messages.deb \
    && rm -rf /tmp/android-messages.deb \
        /var/lib/apt/lists/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# Because we use volume mounting, we want to keep the runtime UID and GID the same
#   as on the host
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID messages \
    && useradd -d /home/messages -s /bin/bash -m messages -u $UID -g $GID \
    && mkdir -p /home/messages/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/messages/.config/gtk-3.0/settings.ini \
    && chown -R $UID:$GID /home/messages/.config \
    && mkdir -p /config \
    && ln -s /config /home/messages/.config/android-messages-desktop

USER messages
# --no-sandbox runs it without containment, we are achieving this by running it in
#   a docker container
# --disable-dev-shm-usage fixes an issue with the shared memory being too small when
#   run via a docker container
CMD [ "AndroidMessages", "--no-sandbox", "--disable-dev-shm-usage" ]
