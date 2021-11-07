from cfgtools.hooks import after
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.system.arch import Pacman

system_packages={Pacman("network-manager-applet")}
files=[
    UserService(f"{__name__}/networkmanager-tray.service"),
]


@after
def start_nm_tray() -> None:
    ensure_service("networkmanager-tray", user=True)
