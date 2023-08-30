FROM ubuntu:20.04

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        libegl1 \
        libfontconfig1 \
        libglx0 \
        libnss3 \
        libopengl0 \
        libsm6 \
        libx11-6 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcomposite1 \
        libxdamage1 \
        libxkbcommon-x11-0 \
        libxkbfile1 \
        libxrandr2 \
        libxtst6 \
        tar \
        xdg-utils \
        xz-utils \
    && rm -rf /var/lib/apt/lists/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

ARG VERSION=6.24.0

RUN mkdir -p /opt/calibre \
    && curl \
        -o /tmp/calibre.txz \
        "https://download.calibre-ebook.com/$VERSION/calibre-$VERSION-x86_64.txz" \
    && tar xvf /tmp/calibre.txz -C /opt/calibre \
    && rm /tmp/calibre.txz \
    && /opt/calibre/calibre_postinstall

# Setup the user for running, this user will own the files used in the mounted
#   config directory
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID calibre \
   && useradd -d /home/calibre -s /bin/bash -m calibre -u $UID -g $GID \
   && mkdir -p /config/config /config/share /home/calibre/.config /home/calibre/.local/share \
   && chown -R $UID:$GID /config \
   && chown -R $UID:$GID /home/calibre/.config \
   && chown -R $UID:$GID /home/calibre/.local/share \
   && ln -s /config/config /home/calibre/.config/calibre \
   && ln -s /config/share /home/calibre/.local/share/calibre-ebook.com

USER calibre
CMD ["calibre"]
