from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, XDG_CONFIG_HOME, normalize
from cfgtools.system.arch import Pacman

import browsers.web_xdg_open
import dropbox
import mpv

NAME = normalize(__name__)

packages={Pacman("streamlink"), Pacman("xclip")}
files=[
    XDGConfigFile(f"{NAME}/config", "streamlink/config"),
    DesktopEntry(f"{NAME}/streamlink.desktop"),
    UserBin(f"{NAME}/streamlink-clipboard.sh", "_streamlink-clipboard"),
    dropbox.EncryptedFile(
        "credentials/streamlink.crunchyroll.gpg",
        XDG_CONFIG_HOME  / "streamlink/config.crunchyroll",
    ),
    browsers.web_xdg_open.SettingsFile(f"{NAME}/web-xdg-open", "streamlink"),
]
