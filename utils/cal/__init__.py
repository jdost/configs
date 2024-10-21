from cfgtools.files import DesktopEntry, XDGConfigFile, XDG_CONFIG_HOME, UserBin, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService

from utils.dropbox import EncryptedFile

ENABLED = True
NAME = normalize(__name__)

packages = {Pacman("calcurse")}
virtualenv = VirtualEnv("gcal-sync", "gcsa", "pytz")
files = [
    UserBin(f"{NAME}/gcal-sync.sh", "gcal-sync"),
    UserService(f"{NAME}/gcal-sync.service"),
    UserService(f"{NAME}/gcal-sync.timer"),
    XDGConfigFile(f"{NAME}/config", "calcurse/conf"),
    DesktopEntry(f"{NAME}/calcurse.desktop"),
    EncryptedFile(
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
