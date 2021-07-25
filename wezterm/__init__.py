from cfgtools.system.arch import AUR, Pacman
from cfgtools.files import XDGConfigFile

pkgs = {Pacman("wezterm"), AUR("./aur/pkgs/ttf-iosevka-ext")}
files = [
    XDGConfigFile(f"{__name__}/wezterm.lua", "wezterm/wezterm.lua"),
]
