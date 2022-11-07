from cfgtools.files import XDGConfigFile, normalize
from cfgtools.system.arch import AUR, Pacman

NAME = normalize(__name__)


packages={Pacman("alacritty"), AUR("./aur/pkgs/ttf-hack-ext")}
files=[
    XDGConfigFile(f"{NAME}/alacritty.yml", "alacritty/alacritty.yml"),
]
