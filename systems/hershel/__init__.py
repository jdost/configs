import apps.zathura
import aur
import browsers.firefox
import browsers.qutebrowser
import cal
import docker
import dropbox
import git
import gpg
import gtk
import languages.python
import scrcpy
import shells.zsh
import streamlink
import tmux
import user_dirs
import utils.ssh
import utils.unclutter
import utils.wallpaper
import vim.neovim
import web_xdg_open
import xorg.window_managers.bspwm
from cfgtools.files import XDG_CONFIG_HOME, File, XinitRC
from cfgtools.system import set_default_shell

web_xdg_open.set_default("firefox")

File("systems/hershel/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/hershel/bspwmrc", XDG_CONFIG_HOME / "bspwm/system")
File("systems/hershel/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/hershel/sxhkdrc", XDG_CONFIG_HOME / "sxhkd/system")
XinitRC("systems/hershel", priority=40)
set_default_shell(shells.zsh.BIN)
