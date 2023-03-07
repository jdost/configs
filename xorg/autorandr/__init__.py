from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service

packages={Pacman("autorandr")}


@after
def enable_autorandr_service() -> None:
    ensure_service("autorandr")
