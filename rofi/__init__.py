from cfgtools.files import UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import AUR, Pacman

NAME = normalize(__name__)

packages = {Pacman("rofi"), AUR("./aur/pkgs/ttf-hack-ext")}
files = [
    XDGConfigFile(f"{NAME}/config.rasi"),
    XDGConfigFile(f"{NAME}/themes/icons_launcher.rasi"),
    XDGConfigFile(f"{NAME}/themes/askpass.rasi"),
    UserBin(f"{NAME}/askpass.sh", "rofi-askpass"),
]
