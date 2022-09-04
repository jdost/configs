#!/bin/zsh
#
# Required in path:
#   - feh
#   - which
#   - curl

set -euo pipefail

# If running headless, grab the first available display, this is a bit naive but
#  allows for things like cron tasks to still set wallpapers
if [[ -z "${DISPLAY:-}" ]]; then
   export DISPLAY=":$(\ls /tmp/.X11-unix/* | head -n1 | sed 's#/tmp/.X11-unix/X##')"
fi

ACTIVE_WALLPAPER="/tmp/wallpaper.$UID"
FOLDER="${WALLPAPER_FOLDER:-$HOME/.local/dropbox/wallpaper}"
[[ -h "$FOLDER" ]] && FOLDER=$(readlink -f "$FOLDER")

help() {
   cat << HELP
wallpaper [action]
  add       -- take remote image URLs from stdin and add them to the collection
  count     -- informative output of size of current collection
  info      -- output internal information for easy visibility
  --latest  -- update image only from most recent batch of wallpapers
  reset     -- sets the most recent wallpaper again, used for restarts
  <default> -- update wallpaper with a random one from collection
HELP
}

# _retrieve is an internal helper function for doing the actual retrieval of a single
#   image URL.  It is meant to handle downloading the image, generating it's
#   fingerprint, verifying the file is unique (i.e. not a different URL from another)
#   and then properly storing it in the folder.
#
# This uses (and expects):
#  - `curl` for downloading the image
_retrieve() {
   local src="$1"
   local suffix="$(echo $src | rev | cut -d'.' -f1 | rev)"
   local tmpfile="$(mktemp /tmp/wallpaper.XXXXX.$suffix)"
   echo -n "Adding $src..."

   curl --silent "$src" > $tmpfile

   if which magick &>/dev/null; then
      local id="$(magick convert $tmpfile -scale 100x100 - | md5sum - | cut -c-8)"
      local dst="$FOLDER/$id.jpg"
      if [[ -e "$dst" ]]; then
         echo "DUPLICATE"
         return 1
      else
         magick convert $tmpfile $dst
         echo "$id.jpg"
      fi
   else
      local id=$(md5sum $tmpfile | cut -c-8)
      local dst="$FOLDER/$id.$suffix"
      if [[ -e "$dst" ]]; then
         echo "DUPLICATE"
         return 1
      fi
      cp $tmpfile "$dst"
      echo "$id.$suffix"
   fi
   rm $tmpfile
}

retrieve() {
   echo "Paste in a target URL per line, use Ctrl-D when finished..."
   local total=0
   while read url; do
      if _retrieve $url; then
         total=$((total+1))
      fi
   done

   echo "Retrieved $total new wallpapers"
}

count() {
   echo "Size of local collection: $(find $FOLDER -type f | wc -l)"
}

info() {
   count
}

switch() {
   case "${1:-all}" in
      "latest")
         # stat is used to output the date from the specified file
         #   it takes the top entry in `ls -t` which is time sorted listing of the
         #   folder, which should be the most recently added file
         # awk is used to strip the timestamp and leave just the date as YYYY-MM-DD
         local latest="$(stat -c %y $FOLDER/$(\ls -t $FOLDER | head -1) | awk '{ print $1 }')"
         # find filtered on files created on the latest date, which should be the
         #   most recent batch of images retrieved
         local selection=(${=$(find $FOLDER -type f -newerct $latest)})
         ;;
      "all")
         local selection=(${=$(find $FOLDER -type f)})
         ;;
   esac

   [[ -h "$ACTIVE_WALLPAPER" ]] && rm "$ACTIVE_WALLPAPER"
   local target="${selection[RANDOM % ${#selection[@]} + 1]}"
   ln -s "$target" "$ACTIVE_WALLPAPER"
   reset_current
}

reset_current() {
   feh --bg-fill --no-fehbg "$ACTIVE_WALLPAPER"
}

case "${1:-}" in
   "-h"|"--help")
      help && exit 0
      ;;
   "add"|"retrieve"|"up"|"upload")
      retrieve
      ;;
   "count"|"c")
      count
      ;;
   "info"|"i")
      info
      ;;
   "--latest")
      switch latest
      ;;
   "reset")
      if [[ ! -e "$ACTIVE_WALLPAPER" ]]; then
        switch
      else
        reset_current
      fi
      ;;
   *)
      switch
      ;;
esac
