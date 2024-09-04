from cfgtools.files import XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service

NAME = normalize(__name__)

packages = {
    Pacman("hypridle"), Pacman("hyprlock"),
}

files = {
    XDGConfigFile(f"{NAME}/hypridle.conf", "hypr/hypridle.conf"),
    UserService(f"{NAME}/hypridle.service", "hypridle.service"),
    XDGConfigFile(f"{NAME}/hyprlock.conf", "hypr/hyprlock.conf"),
}


@after
def enable_hypridle() -> None:
    ensure_service("hypridle.service", user=True)
