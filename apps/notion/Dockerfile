FROM ubuntu:20.04

# The installer is sourced from the project's github release page, so we can define
#   the target version via an arg
ARG VERSION=2.0.11
ARG DEB_RELEASE_URI=https://github.com/davidbailey00/notion-deb-builder/releases/download

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
    && wget --quiet -O /tmp/notion.deb $DEB_RELEASE_URI/v${VERSION}/notion-desktop_${VERSION}_amd64.deb \
    && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends /tmp/notion.deb \
    && rm -rf /tmp/notion.deb \
        /var/lib/apt/lists/* \
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
    && ln -s /config /home/notion/.config/notion-desktop

USER notion
# --no-sandbox runs it without containment, we are achieving this by running it in
#   a docker container
# --disable-dev-shm-usage fixes an issue with the shared memory being too small when
#   run via a docker container
CMD [ "notion-desktop", "--no-sandbox", "--disable-dev-shm-usage" ]
