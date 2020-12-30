from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman

packages = {Pacman("papirus-icon-theme")}
files=[
    XDGConfigFile(f"{__name__}/settings.ini", "gtk-3.0/settings.ini"),
]
