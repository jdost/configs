from cfgtools.files import DesktopEntry, XDGConfigFile, UserBin
from cfgtools.system.arch import AUR, Pacman

import alacritty
import tmux

packages = {Pacman("cmus"), AUR("ncspot")}
files = [
    XDGConfigFile(f"{__name__}/ncspot.toml", "ncspot/config.toml"),
    XDGConfigFile(f"{__name__}/cmus", "cmus/rc"),
    UserBin(f"{__name__}/music-tmux.sh", "music-tmux"),
    DesktopEntry(f"{__name__}/music-sidebar.desktop"),
]

# populate ~/.config/ncspot/credentials.toml from pass?
