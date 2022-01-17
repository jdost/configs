FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        libgtk-3-0 \
        libx11-xcb1 \
    && curl -s https://updates.signal.org/desktop/apt/keys.asc | apt-key add - \
    && echo "deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main" \
            > /etc/apt/sources.list.d/signal.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y signal-desktop\
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# Because we use volume mounting, we want to keep the runtime UID and GID the same
#   as on the host
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID signal \
    && useradd -d /home/signal -s /bin/bash -m signal -u $UID -g $GID \
    && mkdir -p /home/signal/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/signal/.config/gtk-3.0/settings.ini \
    && chown -R $UID:$GID /home/signal/.config \
    && mkdir -p /config && chown -R $UID:$GID /config \
    && ln -s /config /home/signal/.config/Signal

USER signal
# --no-sandbox runs it without containment, we are achieving this by running it in
#   a docker container
# --disable-dev-shm-usage fixes an issue with the shared memory being too small when
#   run via a docker container
CMD [ "signal-desktop", "--no-sandbox", "--disable-dev-shm-usage" ]
