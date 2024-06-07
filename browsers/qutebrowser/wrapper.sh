#!/usr/bin/env bash

set -euo pipefail
# If there is more than one `qutebrowser` result in the path, we need to figure out the
#  precedence and target the proper binary.  This is mainly due to something like
#  this script or a shell alias existing above the actual binary
TARGET_BIN="qutebrowser"
if [[ "$(which $TARGET_BIN)" != "$(which -a $TARGET_BIN)" ]]; then
   ALIASED_LEN=$(which $TARGET_BIN | wc -l)
   BIN=$(which -a $TARGET_BIN | uniq | sed -e "1,$ALIASED_LEN"d | head -n 1)
else
   BIN=$(which $TARGET_BIN)
fi

# Fix HiDPI scaling handling in QT on Wayland
#   see: https://bugreports.qt.io/browse/QTBUG-113574?focusedId=723760&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-723760
if [[ ! -z "${WAYLAND_DISPLAY:-}" ]]; then
    export QT_SCALE_FACTOR_ROUNDING_POLICY=RoundPreferFloor
fi

exec $BIN "$@"
