from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, XDG_CONFIG_HOME
from cfgtools.system.arch import Pacman

import dropbox
import mpv
import web_xdg_open

packages={Pacman("streamlink"), Pacman("xclip")}
files=[
    XDGConfigFile(f"{__name__}/config", "streamlink/config"),
    DesktopEntry(f"{__name__}/streamlink.desktop"),
    UserBin(f"{__name__}/streamlink-clipboard.sh", "_streamlink-clipboard"),
    dropbox.EncryptedFile(
        "credentials/streamlink.crunchyroll.gpg",
        XDG_CONFIG_HOME  / "streamlink/config.crunchyroll",
    ),
    web_xdg_open.SettingsFile(f"{__name__}/web-xdg-open", "streamlink"),
]
