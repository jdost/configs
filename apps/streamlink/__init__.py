import apps.mpv
import browsers.web_xdg_open
from cfgtools.files import XDG_CONFIG_HOME, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from utils import dropbox

NAME = normalize(__name__)

packages={Pacman("streamlink")}
files=[
    XDGConfigFile(f"{NAME}/config", "streamlink/config"),
    dropbox.EncryptedFile(
        "credentials/streamlink.crunchyroll.gpg",
        XDG_CONFIG_HOME  / "streamlink/config.crunchyroll",
    ),
    browsers.web_xdg_open.SettingsFile(f"{NAME}/web-xdg-open", "streamlink"),
]
