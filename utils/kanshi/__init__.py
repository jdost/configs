from cfgtools.files import XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service

NAME = normalize(__name__)

packages = {
    Pacman("kanshi"),
}

files = {
    XDGConfigFile(f"{NAME}/base", "kanshi/config"),
    UserService(f"{NAME}/kanshi.service", "kanshi.service"),
}


@after
def enable_kanshi() -> None:
    ensure_service("kanshi.service", user=True)
