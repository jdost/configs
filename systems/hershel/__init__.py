import aur
import bspwm
import cal
import docker
import dropbox
import firefox
import git
import gpg
import gtk
import python
import qutebrowser
import scrcpy
import ssh
import streamlink
import tmux
import unclutter
import user_dirs
import vim.neovim
import wallpaper
import web_xdg_open
import zathura
import zsh
from cfgtools.files import XDG_CONFIG_HOME, File, XinitRC

web_xdg_open.set_default("firefox")

File("systems/hershel/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/hershel/bspwmrc", XDG_CONFIG_HOME / "bspwm/system")
File("systems/hershel/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/hershel/sxhkdrc", XDG_CONFIG_HOME / "sxhkd/system")
XinitRC("systems/hershel", priority=40)
