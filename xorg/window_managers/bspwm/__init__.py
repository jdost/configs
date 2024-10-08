import apps.alacritty
import rofi
import xorg
import xorg.deadd
import xorg.picom
import xorg.polybar
import xorg.sxhkd
from cfgtools.files import XDGConfigFile, XinitRC, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {Pacman("bspwm"), Pacman("xorg-xsetroot")}
files = [
    XDGConfigFile(f"{NAME}/bspwmrc", "bspwm/bspwmrc"),
    XDGConfigFile(f"{NAME}/polybar", "polybar/bspwm"),
    XinitRC(NAME, priority=99),
]
