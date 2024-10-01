import apps.alacritty
import aur
import auth
import bat
import git
import gpg
import python
import shells.zsh
import utils.docker
import utils.dropbox
import utils.networkmanager
import utils.ssh
import utils.tmux
import utils.unclutter
import utils.user_dirs
import utils.wallpaper
import vim
import xorg.autorandr
import utils.icons.papirus
import xorg.polybar
import xorg.screenlock
import xorg.window_managers.bspwm
from cfgtools.files import HOME, File, XinitRC
from cfgtools.systems import set_default_shell

File("systems/isabelle/polybar", HOME / ".config/polybar/system")
File("systems/isabelle/Xresources", HOME / ".config/xorg/Xresources.system")
XinitRC("systems/isabelle", name="system", priority=40)
set_default_shell(shells.zsh.BIN)
