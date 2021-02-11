from cfgtools.files import File, HOME, XinitRC

import aur
import bat
import bspwm
import docker
import dropbox
import git
import gpg
import gtk
import polybar
import python
import screenlock
import tmux
import unclutter
import user_dirs
import vim
import wallpaper
import zsh

File("systems/anthony/polybar", HOME / ".config/polybar/system")
File("systems/anthony/Xresources", HOME / ".config/xorg/Xresources.system")
File("systems/anthony/bspwm_external_rules.sh", HOME / ".config/bspwm/external_rules")
File("systems/anthony/chromium-flags.conf", HOME / ".config/chromium-flags.conf")
XinitRC("systems/anthony", priority=40)
