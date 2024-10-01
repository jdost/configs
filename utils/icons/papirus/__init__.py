from cfgtools.files import XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {Pacman("papirus-icon-theme")}
files = [
    XDGConfigFile(f"{NAME}/settings.ini", "gtk-3.0/settings.ini"),
]
