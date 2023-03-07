import apps.alacritty
import aur
import auth
import bat
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
import user_dirs
import utils.docker
import utils.ssh
import utils.unclutter
import utils.wallpaper
import vim
import xorg.autorandr
import xorg.window_managers.bspwm
from cfgtools.files import HOME, File, XinitRC
from cfgtools.systems import set_default_shell

File("systems/isabelle/polybar", HOME / ".config/polybar/system")
File("systems/isabelle/Xresources", HOME / ".config/xorg/Xresources.system")
XinitRC("systems/isabelle", name="system", priority=40)
set_default_shell(shells.zsh.BIN)
