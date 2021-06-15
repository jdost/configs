from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile
from cfgtools.system.arch import Pacman

import rofi

packages = {Pacman("maim"),Pacman("which"),Pacman("xclip")}
files = [
    UserBin(f"{__name__}/screencap-menu.sh", "rofi-screencap"),
    XDGConfigFile(f"{__name__}/config.rasi", "rofi/themes/screencap.rasi"),
    DesktopEntry(f"{__name__}/screencap.desktop"),
]
