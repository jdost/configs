from cfgtools.files import XDGConfigFile, XDG_CONFIG_HOME
from cfgtools.system.arch import Pacman

import dropbox

packages={Pacman("mpv"), Pacman("streamlink")}
files=[
    XDGConfigFile(f"{__name__}/config", "streamlink/config"),
    dropbox.EncryptedFile(
        "credentials/streamlink.crunchyroll.gpg",
        XDG_CONFIG_HOME  / "streamlink/config.crunchyroll",
    ),
]
