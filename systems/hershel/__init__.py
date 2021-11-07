import alacritty
import aur
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
import ssh
import streamlink
import tmux
import unclutter
import user_dirs
import vim.neovim
import wallpaper
import zathura
import zsh
from cfgtools.files import XDG_CONFIG_HOME, File, XinitRC

File("systems/hershel/polybar", XDG_CONFIG_HOME / "polybar/system")
File("systems/hershel/bspwmrc", XDG_CONFIG_HOME / "bspwm/system")
File("systems/hershel/bspwm_external_rules.sh", XDG_CONFIG_HOME / "bspwm/external_rules")
File("systems/hershel/sxhkdrc", XDG_CONFIG_HOME / "sxhkd/system")
XinitRC("systems/hershel", priority=40)
