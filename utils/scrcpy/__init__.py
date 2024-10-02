from cfgtools.files import DesktopEntry, UserBin, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.utils import add_group, hide_xdg_entry

NAME = normalize(__name__)

pkgs = {Pacman("scrcpy"), Pacman("android-tools")}
files = [
    UserBin(f"{NAME}/wrapper.sh", "scrcpy"),
    DesktopEntry(f"{NAME}/scrcpy.desktop"),
]


@after
def hide_unwanted_xdg_entries() -> None:
    hide_xdg_entry("scrcpy-console")


@after
def add_to_adb_group() -> None:
    add_group("adbusers")
