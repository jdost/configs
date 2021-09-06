from cfgtools.files import DesktopEntry, XDGConfigFile, XDG_CONFIG_HOME, UserBin
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService

import dropbox

ENABLED = True

packages = {Pacman("calcurse")}
virtualenv = VirtualEnv("gcal-sync", "gcsa")
files = [
    UserBin(f"{__name__}/gcal-sync.sh", "gcal-sync"),
    UserService(f"{__name__}/gcal-sync.service"),
    UserService(f"{__name__}/gcal-sync.timer"),
    XDGConfigFile(f"{__name__}/config", "calcurse/conf"),
    DesktopEntry(f"{__name__}/calcurse.desktop"),
    dropbox.EncryptedFile(
        "credentials/gcal-sync.json.gpg",
        XDG_CONFIG_HOME / "calcurse/credentials.json",
    ),
]


@after
def enable_sync_timer() -> None:
    global ENABLED
    if not ENABLED:
        return

    ensure_service("gcal-sync.timer", user=True)
