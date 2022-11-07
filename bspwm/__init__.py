from cfgtools.files import XinitRC, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

import apps.alacritty
import deadd
import picom
import polybar
import rofi
import sxhkd
import xorg

NAME = normalize(__name__)

packages = {Pacman("bspwm"), Pacman("xorg-xsetroot")}
files = [
    XDGConfigFile(f"{NAME}/bspwmrc"),
    XDGConfigFile(f"{NAME}/polybar", "polybar/bspwm"),
    XinitRC(NAME, priority=99),
]
