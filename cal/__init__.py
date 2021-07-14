from cfgtools.files import XDGConfigFile, XDG_CONFIG_HOME, UserBin
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService

import dropbox

packages = {Pacman("calcurse")}
virtualenv = VirtualEnv("gcal-sync", "gcsa")
files = [
    UserBin(f"{__name__}/gcal-sync.py", "gcal-sync"),
    UserService(f"{__name__}/gcal-sync.service"),
    UserService(f"{__name__}/gcal-sync.timer"),
    XDGConfigFile(f"{__name__}/config", "calcurse/conf"),
    dropbox.EncryptedFile(
        "credentials/gcal-sync.json.gpg",
        XDG_CONFIG_HOME / "calcurse/credentials.json",
    ),
]


@after
def enable_sync_timer() -> None:
    ensure_service("gcal-sync.timer", user=True)
