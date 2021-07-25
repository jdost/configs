from cfgtools.system.arch import Pacman, AUR
from cfgtools.files import DesktopEntry, UserBin

pkgs = {AUR("scrcpy"), Pacman("android-tools")}
files = [
    UserBin(f"{__name__}/wrapper.sh", "scrcpy"),
    DesktopEntry(f"{__name__}/scrcpy.desktop"),
]
