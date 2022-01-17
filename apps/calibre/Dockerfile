FROM ubuntu:20.04

RUN apt-get update \
   && apt-get install -y --no-install-recommends \
      calibre \
   && rm -rf /var/lib/apt/lists/* \
      /var/cache/apt/* \
      /var/log/* \
      /usr/share/man \
      /usr/share/doc

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
