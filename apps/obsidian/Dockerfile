from ubuntu:20.04

ARG VERSION="1.1.8"
ARG APPIMAGE_RELEASE_URI="https://github.com/obsidianmd/obsidian-releases/releases/download"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libasound2 \
        libgbm1 \
        libgtk-3-0 \
        libnss3 \
        libx11-xcb1 \
        wget \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

RUN wget --quiet -O "/tmp/obsidian.appimage" \
        "$APPIMAGE_RELEASE_URI/v$VERSION/Obsidian-$VERSION.AppImage" \
    && chmod +x /tmp/obsidian.appimage

ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID obsidian \
    && useradd -d /home/obsidian -s /bin/bash -m obsidian -u $UID -g $GID \
    && mkdir -p /home/obsidian/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/obsidian/.config/gtk-3.0/settings.ini \
    && chown -R $UID:$GID /home/obsidian/.config \
    && mkdir -p /config && chown -R $UID:$GID /config \
    && ln -s /config /home/obsidian/.config/obsidian \
    && mkdir -p /data && chown -R $UID:$GID /data \
    && ln -s /data /home/obsidian/vaults

USER obsidian
# --appimage-extract-and-run will skip the FUSE requirement and just run natively
# --no-sandbox runs it without containment, which the container is facilitating
# --disable-dev-shm-usage avoids weird issues with permissions and shared memory
CMD [ "/tmp/obsidian.appimage", \
      "--appimage-extract-and-run", \
      "--no-sandbox", \
      "--disable-dev-shm-usage" ]
