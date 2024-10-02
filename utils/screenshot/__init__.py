import rofi
import utils.icons.papirus
from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {Pacman("which")}
files = [
    UserBin(f"{NAME}/screencap-menu.sh", "rofi-screencap"),
    XDGConfigFile(f"{NAME}/config.rasi", "rofi/themes/screencap.rasi"),
    DesktopEntry(f"{NAME}/screencap.desktop"),
]
