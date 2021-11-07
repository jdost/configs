from cfgtools.files import File, HOME, XinitRC

import alacritty
import aur
import auth
import autorandr
import bat
import bspwm
import docker
import dropbox
import git
import gpg
import gtk
import networkmanager
import polybar
import python
import screenlock
import ssh
import tmux
import unclutter
import user_dirs
import vim
import wallpaper
import zsh

File("systems/isabelle/polybar", HOME / ".config/polybar/system")
File("systems/isabelle/Xresources", HOME / ".config/xorg/Xresources.system")
XinitRC("systems/isabelle", name="system", priority=40)
