import apps.alacritty
import aur
import auth
import bat
import git
import gpg
import networkmanager
import python
import screenlock
import shells.zsh
import utils.docker
import utils.dropbox
import utils.ssh
import utils.tmux
import utils.unclutter
import utils.user_dirs
import utils.wallpaper
import vim
import xorg.autorandr
import xorg.icons.papirus
import xorg.polybar
import xorg.window_managers.bspwm
from cfgtools.files import HOME, File, XinitRC
from cfgtools.systems import set_default_shell

File("systems/isabelle/polybar", HOME / ".config/polybar/system")
File("systems/isabelle/Xresources", HOME / ".config/xorg/Xresources.system")
XinitRC("systems/isabelle", name="system", priority=40)
set_default_shell(shells.zsh.BIN)
