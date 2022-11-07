import apps.alacritty
import deadd
import picom
import polybar
import rofi
import unclutter
import xorg
from cfgtools.files import HOME, File, XDGConfigFile, XinitRC, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

pkgs = {
    Pacman("xmonad"), Pacman("xmonad-contrib"),
    Pacman("xorg-xsetroot"), Pacman("xdotool"),
}

files = [
    File(f"{NAME}/xmonad.hs", HOME / ".xmonad/xmonad.hs"),
    File(f"{NAME}/lib", HOME / ".xmonad/lib"),
    XDGConfigFile(f"{NAME}/polybar", "polybar/xmonad"),
    XinitRC(NAME, priority=99),
]
