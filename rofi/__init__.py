from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import AUR, Pacman

packages = {Pacman("rofi"), AUR("./aur/pkgs/ttf-hack-ext")}
files = [
    XDGConfigFile("rofi/default.rasi"),
    XDGConfigFile("rofi/config.rasi"),
    XDGConfigFile("rofi/scripts/totp"),
    XDGConfigFile("rofi/scripts/pass"),
]
