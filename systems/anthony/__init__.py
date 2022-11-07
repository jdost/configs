from cfgtools.files import File, HOME, XDG_CONFIG_HOME, XinitRC
from cfgtools.system import set_default_shell

import apps.alacritty
import apps.zathura
import aur
import autorandr
import bspwm
import cal
import docker
import dropbox
import git
import gpg
import gtk
import polybar
import python
import qutebrowser
import screenlock
import shells.zsh
import streamlink
import tmux
import user_dirs
import utils.bat
import utils.ssh
import utils.unclutter
import utils.wallpaper
import vim

cal.ENABLED = False

File("systems/anthony/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/anthony/Xresources", XDG_CONFIG_HOME / "xorg/Xresources.system")
File("systems/anthony/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/anthony/chromium-flags.conf", XDG_CONFIG_HOME / "chromium-flags.conf")
XinitRC("systems/anthony", priority=40)
File("systems/anthony/drirc", HOME / ".drirc")
set_default_shell(shells.zsh.BIN)
