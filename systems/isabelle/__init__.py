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
import shells.zsh
import tmux
import unclutter
import user_dirs
import utils.ssh
import vim
import wallpaper
from cfgtools.files import HOME, File, XinitRC
from cfgtools.systems import set_default_shell

File("systems/isabelle/polybar", HOME / ".config/polybar/system")
File("systems/isabelle/Xresources", HOME / ".config/xorg/Xresources.system")
XinitRC("systems/isabelle", name="system", priority=40)
set_default_shell(shells.zsh.BIN)
