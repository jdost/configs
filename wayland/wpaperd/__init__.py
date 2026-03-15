from cfgtools.files import XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service

NAME = normalize(__name__)

packages = {
    Pacman("wpaperd"),
}
files = {
    XDGConfigFile(f"{NAME}/config.toml", "wpaperd/config.toml"),
    UserService(f"{NAME}/wpaperd.service", "wpaperd.service"),
}


@after
def enable_wpaperd() -> None:
    ensure_service("wpaperd.service", user=True)
