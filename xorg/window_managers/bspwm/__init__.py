import apps.alacritty
import deadd
import rofi
import sxhkd
import xorg
import xorg.picom
import xorg.polybar
from cfgtools.files import XDGConfigFile, XinitRC, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {Pacman("bspwm"), Pacman("xorg-xsetroot")}
files = [
    XDGConfigFile(f"{NAME}/bspwmrc", "bspwm/bspwmrc"),
    XDGConfigFile(f"{NAME}/polybar", "polybar/bspwm"),
    XinitRC(NAME, priority=99),
]
