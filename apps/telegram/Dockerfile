FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        telegram-desktop \
    && rm -rf /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# Because we use volume mounting, we want to keep the runtime UID and GID the same
#   as on the host
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID telegram \
    && useradd -d /home/telegram -s /bin/bash -m telegram -u $UID -g $GID \
    && mkdir -p /home/telegram/.config/gtk-3.0 \
    && printf "[Settings]\ngtk-application-prefer-dark-theme = true\n" \
        > /home/telegram/.config/gtk-3.0/settings.ini \
    && mkdir -p /home/telegram/.local/share \
    && chown -R $UID:$GID /home/telegram/.local \
    && mkdir -p /config && chown -R $UID:$GID /config \
    && ln -s /config /home/telegram/.local/share/TelegramDesktop

USER telegram
CMD [ "telegram-desktop" ]
