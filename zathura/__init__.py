from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman, AUR

system_packages = {
    Pacman("zathura"), Pacman("zathura-pdf-mupdf"),
    AUR("./aur/pkgs/ttf-hack-ext"),
}
files = [
    XDGConfigFile("zathura/zathurarc"),
]
