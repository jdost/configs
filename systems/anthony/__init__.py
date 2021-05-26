from cfgtools.files import File, XDG_CONFIG_HOME, XinitRC

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

File("systems/anthony/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/anthony/Xresources", XDG_CONFIG_HOME / "xorg/Xresources.system")
File("systems/anthony/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/anthony/chromium-flags.conf", XDG_CONFIG_HOME / "chromium-flags.conf")
XinitRC("systems/anthony", priority=40)
