from cfgtools.system.arch import Pacman, AUR
from cfgtools.files import DesktopEntry, UserBin, normalize

NAME = normalize(__name__)

pkgs = {AUR("scrcpy"), Pacman("android-tools")}
files = [
    UserBin(f"{NAME}/wrapper.sh", "scrcpy"),
    DesktopEntry(f"{NAME}/scrcpy.desktop"),
]
