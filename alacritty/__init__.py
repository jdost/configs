from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import AUR, Pacman


packages={Pacman("alacritty"), AUR("./aur/pkgs/ttf-hack-ext")}
files=[
    XDGConfigFile("alacritty/alacritty.yml"),
]
