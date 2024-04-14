FROM archlinux:base-devel

RUN \
   --mount=type=cache,target=/var/cache/pacman/pkg/ \
   echo "ParallelDownloads=5" >> /etc/pacman.conf \
   && pacman -Sy --noconfirm archlinux-keyring \
   && pacman -Syu --noconfirm \
      base-devel \
      git

# Setup the user for running, this user will own the files used in the mounted
#   config directory
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID builder \
   && useradd -d /build -s /bin/bash -m builder -u $UID -g $GID \
   && mkdir -p /pkgs && chown -R $UID:$GID /pkgs \
   && mkdir -p /src && chown -R $UID:$GID /src \
   && echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers

ADD entrypoint /entrypoint
USER builder
ENTRYPOINT ["/entrypoint"]
