from cfgtools.system.arch import Pacman
from cfgtools.files import XDGConfigFile

pkgs = {Pacman("wezterm")}
files = [
    XDGConfigFile(f"{__name__}/wezterm.lua", "wezterm/wezterm.lua"),
]
