from cfgtools.files import File, XDG_CONFIG_HOME, XinitRC

import aur
import bspwm
import dropbox
import git
import gpg
import python
import tmux
import unclutter
import user_dirs
import wallpaper
import zsh

File(f"systems/hershel/polybar", XDG_CONFIG_HOME / "polybar/system")
File(f"systems/hershel/bspwmrc", XDG_CONFIG_HOME / "bspwm/system")
File(f"systems/hershel/sxhkdrc", XDG_CONFIG_HOME / "sxhkd/system")
XinitRC("systems/hershel", priority=40)
