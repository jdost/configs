from pathlib import Path

import alacritty
import deadd
import picom
import polybar
import rofi
import unclutter
import xorg
from cfgtools.files import File, XDGConfigFile, XinitRC
from cfgtools.system.arch import Pacman

pkgs = {
    Pacman("xmonad"), Pacman("xmonad-contrib"),
    Pacman("xorg-xsetroot"), Pacman("xdotool"),
}

files = [
    File(f"{__name__}/xmonad.hs", Path.home() / ".xmonad/xmonad.hs"),
    File(f"{__name__}/lib", Path.home() / ".xmonad/lib"),
    XDGConfigFile(f"{__name__}/polybar", "polybar/{__name__}"),
    XinitRC(__name__, priority=99),
]
