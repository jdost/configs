#!/usr/bin/env bash

# Docker wrapper to provide some additional helper functions to the CLI

set -euo pipefail
# If there is more than one `docker` result in the path, we need to figure out the
#  precedence and target the proper binary.  This is mainly due to something like
#  this script or a shell alias existing above the actual binary
TARGET_BIN="docker"
if [[ "$(which $TARGET_BIN)" != "$(which -a $TARGET_BIN)" ]]; then
   ALIASED_LEN=$(which $TARGET_BIN | wc -l)
   BIN=$(which -a $TARGET_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
   BIN=$(which $TARGET_BIN)
fi

export DOCKER_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/docker"

clean() {
   # docker ps -- List all created containers (even those not running)
   #  grep -v -- remove the header line
   #  awk -- print the second column (the image name)
   #  sort+uniq -- trim to uniques
   local used_images=$(
      $BIN ps --all --format=json \
         | jq ".Image" \
         | sort | uniq
   )
   # Remove containers using the old images, i.e. have a `<none>` tag, meaning it
   # has been re-applied to a newer image
   #  docker images -a -- this includes intermediate images/layers
   for image in $($BIN images --all --format=json | grep "<none>"); do
      # If the untagged image is still in use on created containers, these
      # containers need to be removed as well
      if echo "$used_images" | grep "$image" &>/dev/null; then
         # The image is being used by a container
         #  docker ps -- List all created containers (even those not running)
         #  grep -- only get the containers with untagged image
         #  awk -- strip to only the container id
         #  xargs docker -- remove the container with the old image
         $BIN ps -a \
            | grep $image \
            | awk '{ print $1 }' \
            | xargs $BIN rm
      fi
   done

   # If there are any top level images that remain untagged, remove them
   if $BIN images | grep "<none>" &> /dev/null; then
      # docker images -- list images
      # grep -- filter only untagged images
      # awk -- get the image id (third column)
      # xargs docker rmi -- remove the image
      $BIN images \
         | grep "<none>" \
         | awk '{ print $1 }' \
         | xargs $BIN rmi
   fi
}

ncurses() {
    local lazydocker_path="$HOME/.local/bin/lazydocker"
    if [[ ! -x "$lazydocker_path" ]]; then
        # prepare the download URL
        local repo="jesseduffield/lazydocker"
        local version=$(curl -L -s -H 'Accept: application/json' https://github.com/$repo/releases/latest | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/')
        local github_file="lazydocker_${version//v/}_$(uname -s)_x86.tar.gz"
        local url="https://github.com/$repo/releases/download/${version}/${github_file}"

        # install/update the local binary
        curl -L -o lazydocker.tar.gz $url
        tar xzvf lazydocker.tar.gz lazydocker
        mv -f lazydocker ${lazydocker_path}
        rm lazydocker.tar.gz
    fi
    exec $lazydocker_path
}

inspect() {
    local dive_path="$HOME/.local/bin/dive"
    if [[ ! -x "$dive_path" ]]; then
        local repo="wagoodman/dive"
        local version=$(curl -L -s -H 'Accept: application/json' https://github.com/$repo/releases/latest | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/')
        local github_file="dive_${version//v/}_$(uname -s)_amd64.tar.gz"
        local url="https://github.com/$repo/releases/download/${version}/${github_file}"

        # install/update the local binary
        curl -L -o dive.tar.gz $url
        tar xzvf dive.tar.gz dive
        mv -f dive ${dive_path}
        rm dive.tar.gz
    fi
    exec $dive_path "$@"
}


case "${1:-}" in
   "clean")
      clean
      ;;
   "stop-all")
      # docker ps -- list running containers
      # grep -- strip off the header row
      # awk -- filter only the first column (container id)
      # xargs docker -- stop each container
      $BIN ps \
         | grep -v "CONTAINER" \
         | awk '{ print $1 }' \
         | xargs $BIN stop
      ;;
   "dive"|"inspect-image")
      shift
      inspect "$@"
      ;;
   "--raw") # Provides a bypass, will avoid the above overrides
      shift
      exec $BIN "$@"
      ;;
   "") # without any arguments, use the ncurses client
       ncurses
       ;;
   *)
      exec $BIN "$@"
      ;;
esac
