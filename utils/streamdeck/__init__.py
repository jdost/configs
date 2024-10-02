from cfgtools.files import DesktopEntry, UserBin, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import UserService, ensure_service

virtualenv = VirtualEnv("streamdeck", "streamdeck-linux-gui")
NAME = normalize(__name__)

pkgs={Pacman("hidapi"), Pacman("qt6-base")}
files=[
    DesktopEntry(f"{NAME}/streamdeck.desktop"),
    UserBin(virtualenv.location / "bin/streamdeck", "streamdeck"),
    UserService(f"{NAME}/streamdeck.service"),
]


@after
def enable_streamdeck_service() -> None:
    ensure_service("streamdeck", user=True)
