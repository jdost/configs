FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        remmina \
        remmina-plugin-rdp \
        remmina-plugin-secret \
        remmina-plugin-vnc \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# Because we use volume mounting, we want to keep the runtime UID and GID the same
#   as on the host
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID remmina \
    && useradd -d /home/remmina -s /bin/bash -m remmina -u $UID -g $GID \
    && mkdir -p /home/remmina/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/remmina/.config/gtk-3.0/settings.ini \
    && chown -R $UID:$GID /home/remmina/.config \
    && mkdir -p /config/config /config/local \
    && ln -s /config/config /home/remmina/.config/remmina \
    && mkdir -p /home/remmina/.local/share \
    && chown -R $UID:$GID /home/remmina/.local \
    && ln -s /config/local /home/remmina/.local/share/remmina

USER remmina
CMD [ "remmina" ]
