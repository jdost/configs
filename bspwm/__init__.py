from cfgtools.files import XinitRC, XDGConfigFile
from cfgtools.system.arch import Pacman

import alacritty
import deadd
import picom
import rofi
import sxhkd
import xorg

packages = {Pacman("bspwm"), Pacman("xorg-xsetroot")}
files = [
    XDGConfigFile("bspwm/bspwmrc"),
    XinitRC(__name__, priority=99),
]
