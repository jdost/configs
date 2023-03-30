from cfgtools.files import UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR, Pacman
from cfgtools.utils import hide_xdg_entry

NAME = normalize(__name__)

packages = {Pacman("rofi"), AUR("./aur/pkgs/ttf-hack-ext")}
files = [
    XDGConfigFile(f"{NAME}/config.rasi"),
    XDGConfigFile(f"{NAME}/themes/icons_launcher.rasi"),
    XDGConfigFile(f"{NAME}/themes/askpass.rasi"),
    UserBin(f"{NAME}/askpass.sh", "rofi-askpass"),
]


@after
def hide_unwanted_mpv_entries() -> None:
    [hide_xdg_entry(e) for e in ["rofi", "rofi-theme-selector"]]
