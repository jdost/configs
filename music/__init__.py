from cfgtools.files import DesktopEntry, XDG_CONFIG_HOME, XDGConfigFile, UserBin, normalize
from cfgtools.system.arch import AUR, Pacman

import apps.alacritty
import utils.tmux
from utils import dropbox

NAME = normalize(__name__)

packages = {Pacman("cmus"), AUR("ncspot")}
files = [
    XDGConfigFile(f"{NAME}/ncspot.toml", "ncspot/config.toml"),
    XDGConfigFile(f"{NAME}/cmus", "cmus/rc"),
    XDGConfigFile(f"{NAME}/cmus.theme", "cmus/local.theme"),
    UserBin(f"{NAME}/music-tmux.sh", "music-tmux"),
    UserBin(f"{NAME}/playerctl-wrapper.sh", "playerctl"),
    DesktopEntry(f"{NAME}/music-sidebar.desktop"),
    dropbox.EncryptedFile(
        "credentials/ncspot.toml.gpg",
        XDG_CONFIG_HOME / "ncspot/credentials.toml",
    ),
]
