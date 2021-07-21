from cfgtools.files import DesktopEntry, XDG_CONFIG_HOME, XDGConfigFile, UserBin
from cfgtools.system.arch import AUR, Pacman

import alacritty
import tmux
import dropbox

packages = {Pacman("cmus"), AUR("ncspot")}
files = [
    XDGConfigFile(f"{__name__}/ncspot.toml", "ncspot/config.toml"),
    XDGConfigFile(f"{__name__}/cmus", "cmus/rc"),
    UserBin(f"{__name__}/music-tmux.sh", "music-tmux"),
    UserBin(f"{__name__}/playerctl-wrapper.sh", "playerctl"),
    DesktopEntry(f"{__name__}/music-sidebar.desktop"),
    dropbox.EncryptedFile(
        "credentials/ncspot.toml.gpg",
        XDG_CONFIG_HOME / "ncspot/credentials.toml",
    ),
]

# populate ~/.config/ncspot/credentials.toml from pass?
