from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import AUR, Pacman

packages = {Pacman("rofi"), AUR("./aur/pkgs/ttf-hack-ext")}
files = [
    XDGConfigFile("rofi/config.rasi"),
    XDGConfigFile("rofi/themes/icons_launcher.rasi"),
]
