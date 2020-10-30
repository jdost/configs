#!/usr/bin/env bash

set -euo pipefail

# Use xsecurelock if possible
if which xsecurelock &>/dev/null; then
   # configure xsecurelock with envvars
   if [[ -x "/usr/lib/xsecurelock/saver_mpv-cinemagraph" ]]; then
      # Customized verison of the mpv saver, loops a single file, either defined
      #   via the _VIDEO_FILE envvar or taken from the directory (if it is a
      #   directory)
      export XSECURELOCK_SAVER=saver_mpv-cinemagraph
      export XSECURELOCK_VIDEO_FILE="$HOME/.local/dropbox/cinemagraphs"
   elif which mpv &>/dev/null; then
      # If mpv is available, have it do a slideshow of all wallpapers
      export XSECURELOCK_SAVER=saver_mpv
      export XSECURELOCK_IMAGE_DURATION_SECONDS=3
      export XSECURELOCK_LIST_VIDEOS_COMMAND="find $HOME/.local/dropbox/wallpaper -type f"
   else
      export XSECURELOCK_SAVER=saver_blank
   fi

   export XSECURELOCK_PAM_SERVICE=system-local-login
   export XSECURELOCK_DISCARD_FIRST_KEYPRESS=0
   export XSECURELOCK_SHOW_DATETIME=1
   exec xsecurelock
fi
