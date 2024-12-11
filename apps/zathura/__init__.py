from cfgtools.files import UserProfile, XDGConfigFile, normalize
from cfgtools.system.arch import AUR, Pacman

NAME = normalize(__name__)

system_packages = {
    Pacman("zathura"), Pacman("zathura-pdf-mupdf"),
    AUR("./aur/pkgs/ttf-hack-ext"),
}
files = [
    XDGConfigFile("apps/zathura/zathurarc", "zathura/zathurarc"),
    UserProfile(NAME, "zathura"),
]
