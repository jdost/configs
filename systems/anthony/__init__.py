from cfgtools.files import File, HOME, XDG_CONFIG_HOME, XinitRC

import alacritty
import aur
import autorandr
import bat
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
import ssh
import streamlink
import tmux
import unclutter
import user_dirs
import vim
import wallpaper
import zathura
import zsh

File("systems/anthony/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/anthony/Xresources", XDG_CONFIG_HOME / "xorg/Xresources.system")
File("systems/anthony/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/anthony/chromium-flags.conf", XDG_CONFIG_HOME / "chromium-flags.conf")
XinitRC("systems/anthony", priority=40)
File("systems/anthony/drirc", HOME / ".drirc")
