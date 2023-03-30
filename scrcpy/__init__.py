from cfgtools.files import DesktopEntry, UserBin, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR, Pacman
from cfgtools.utils import hide_xdg_entry

NAME = normalize(__name__)

pkgs = {AUR("scrcpy"), Pacman("android-tools")}
files = [
    UserBin(f"{NAME}/wrapper.sh", "scrcpy"),
    DesktopEntry(f"{NAME}/scrcpy.desktop"),
]


@after
def hide_unwanted_xdg_entries() -> None:
    hide_xdg_entry("scrcpy-console")
