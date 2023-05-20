from cfgtools.system.arch import AUR, Pacman
from cfgtools.files import XDGConfigFile, normalize

import rofi

NAME = normalize(__name__)

pkgs = {Pacman("wezterm"), AUR("./aur/pkgs/ttf-iosevka-ext")}
files = [
    XDGConfigFile(f"{NAME}/wezterm.lua", "wezterm/wezterm.lua"),
    rofi.RofiModule(f"{NAME}/rofi.rasi", "wezterm"),
]
