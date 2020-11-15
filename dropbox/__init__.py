from cfgtools.files import UserBin
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService

packages = {Pacman("qt5-base")}
virtualenv = VirtualEnv("maestral", "maestral", "maestral-qt")
files = [
    UserBin(virtualenv.location / "bin/maestral", "maestral"),
    UserService(f"{__name__}/dropbox.service"),
]


@after
def enable_dropbox_service() -> None:
    ensure_service("dropbox", user=True)
