#!/bin/sh

# Docker wrapper to provide some additional helper functions to the CLI

set -euo pipefail
# If there is more than one `docker` result in the path, we need to figure out the
#  precedence and target the proper binary.  This is mainly due to something like
#  this script or a shell alias existing above the actual binary
if [[ "$(which docker)" != "$(which -a docker)" ]]; then
   ALIASED_DOCKER_LEN=$(which docker | wc -l)
   DOCKER_BIN=$(which -a docker | sed -e "1,$ALIASED_DOCKER_LEN"d | head -n 1)
else
   DOCKER_BIN=$(which docker)
fi

clean() {
   # docker ps -- List all created containers (even those not running)
   #  grep -v -- remove the header line
   #  awk -- print the second column (the image name)
   #  sort+uniq -- trim to uniques
   local used_images=$(
      $DOCKER_BIN ps -a \
         | grep -v "CONTAINER_ID" \
         | awk '{ print $2 }' \
         | sort | uniq
   )
   # Remove containers using the old images, i.e. have a `<none>` tag, meaning it
   # has been re-applied to a newer image
   #  docker images -a -- this includes intermediate images/layers
   for image in $($DOCKER_BIN images -a | grep "<none>"); do
      # If the untagged image is still in use on created containers, these
      # containers need to be removed as well
      if echo "$used_images" | grep "$image" &>/dev/null; then
         # The image is being used by a container
         #  docker ps -- List all created containers (even those not running)
         #  grep -- only get the containers with untagged image
         #  awk -- strip to only the container id
         #  xargs docker -- remove the container with the old image
         $DOCKER_BIN ps -a \
            | grep $image \
            | awk '{ print $1 }' \
            | xargs $DOCKER_BIN rm
      fi
   done

   # If there are any top level images that remain untagged, remove them
   if $DOCKER_BIN images | grep "<none>"; then
      # docker images -- list images
      # grep -- filter only untagged images
      # awk -- get the image id (third column)
      # xargs docker rmi -- remove the image
      $DOCKER_BIN images \
         | grep "<none>" \
         | awk '{ print $3 }' \
         | xargs $DOCKER_BIN rmi
   fi
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
      $DOCKER_BIN ps \
         | grep -v "CONTAINER" \
         | awk '{ print $1 }' \
         | xargs $DOCKER_BIN stop
      ;;
   "--raw") # Provides a bypass, will avoid the above overrides
      shift
      exec $DOCKER_BIN "$@"
      ;;
   *)
      exec $DOCKER_BIN "$@"
      ;;
esac
