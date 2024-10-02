import apps.alacritty
import apps.streamlink
import apps.zathura
import aur
import browsers.qutebrowser
import git
import gpg
import gtk
import languages.python
import shells.zsh
import utils.bat
import utils.cal
import utils.docker
import utils.dropbox.wayland
import utils.icons.papirus
import utils.opensnitch
import utils.screenshot.wayland
import utils.ssh
import utils.tmux
import utils.unclutter
import utils.user_dirs
import utils.wallpaper
import vim
import xorg.autorandr
import xorg.polybar
import xorg.screenlock
import xorg.window_managers.bspwm
from cfgtools.files import HOME, XDG_CONFIG_HOME, File, XinitRC
from cfgtools.system import set_default_shell

utils.cal.ENABLED = False
xorg.polybar.set_icon_font("fluent")
set_default_shell(shells.zsh.BIN)

File("systems/anthony/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/anthony/Xresources", XDG_CONFIG_HOME / "xorg/Xresources.system")
File("systems/anthony/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/anthony/chromium-flags.conf", XDG_CONFIG_HOME / "chromium-flags.conf")
XinitRC("systems/anthony", priority=40)
File("systems/anthony/drirc", HOME / ".drirc")
