FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        libasound2 \
        libatk-bridge2.0-0 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libxshmfence1 \
        sudo \
    && apt-key \
        --keyring /usr/share/keyrings/1password.gpg adv \
        --keyserver keyserver.ubuntu.com \
        --recv-keys 3FEF9748469ADBE15DA7CA80AC2D62742012EA22 \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/1password.gpg] https://downloads.1password.com/linux/debian edge main" \
            > /etc/apt/sources.list.d/1password.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        1password \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# Because we use volume mounting, we want to keep the runtime UID and GID the same
#   as on the host
ARG UID=1000
ARG GID=1000

RUN useradd -d /home/1password -s /bin/bash -m 1password -u $UID -g $GID \
    && mkdir -p /home/1password/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/1password/.config/gtk-3.0/settings.ini \
    && chown -R $UID:$GID /home/1password/.config \
    && mkdir -p /config && chown -R $UID:$GID /config \
    && ln -s /config /home/1password/.config/1password

USER 1password
# --no-sandbox runs it without containment, we are achieving this by running it in
#   a docker container
CMD [ "1password", "--no-sandbox", "--disable-dev-shm-usage" ]
