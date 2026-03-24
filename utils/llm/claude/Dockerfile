FROM ubuntu:24.04 AS read_only

RUN \
    --mount=type=cache,target=/var/cache/apt \
    apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        git \
        npm \
    && rm -rf /var/lib/apt/lists/* \
        /var/log/* \
        /usr/share/man \
        /usr/share/doc

# For write mode, we need to be able to write to the mounted paths, so we need to run
#   with the same owner permissions to avoid permissions issues in the parent container
ARG UID=1000
ARG GID=1000

# Cache the user+group creation and image cleanup, this is probably static after first build
RUN userdel ubuntu \
   && groupadd -g $GID claude \
   && useradd -d /home/claude -s /bin/bash -m claude -u $UID -g $GID

ARG VERSION=2.1.9
ARG ARCHITECTURE=x64

RUN curl -o /usr/local/bin/claude \
        https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/${VERSION}/linux-${ARCHITECTURE}/claude \
    && chmod +x /usr/local/bin/claude

# Setup config persistence across runs
RUN mkdir /config \
   && mkdir /config/claude && chown $UID:$GID /config/claude \
   && ln -s /config/claude /home/claude/.claude \
   && mkdir /config/xdg_claude && chown $UID:$GID /config/xdg_claude \
   && mkdir /home/claude/.config && chown $UID:$GID /home/claude/.config \
   && ln -s /config/xdg_claude /home/claude/.config/claude \
   && mkdir /code && chown $UID:$GID /code \
   && mkdir -p /home/claude/.local/bin \
   && chown $UID:$GID /home/claude/.local && chown $UID:$GID /home/claude/.local/bin \
   && ln -s /usr/local/bin/claude /home/claude/.local/bin/claude \
   && chown $UID:$GID /home/claude/.local/bin/claude

# We don't want claude trying to auto update
ENV NPM_CONFIG_PREFIX="/nonexistent"
ENV DISABLE_AUTOUPDATER=1
# Disable Telemetry
ENV CLAUDE_CODE_ENABLE_TELEMETRY=0
# Fix Path to stop nagging
ENV PATH=/home/claude/.local/bin:$PATH

USER $UID:$GID
WORKDIR /code

CMD ["/usr/local/bin/claude"]
