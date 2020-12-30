from cfgtools.files import File, HOME, XinitRC

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

File(f"systems/hershel/polybar", HOME / ".config/polybar/system")
File(f"systems/hershel/bspwmrc", HOME / ".config/bspwm/system")
File(f"systems/hershel/sxhkdrc", HOME / ".config/sxhkd/system")
XinitRC("systems/hershel", priority=40)
