from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

import rofi

NAME = normalize(__name__)

packages = {Pacman("maim"),Pacman("which"),Pacman("xclip")}
files = [
    UserBin(f"{NAME}/screencap-menu.sh", "rofi-screencap"),
    XDGConfigFile(f"{NAME}/config.rasi", "rofi/themes/screencap.rasi"),
    DesktopEntry(f"{NAME}/screencap.desktop"),
]
