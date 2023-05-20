from cfgtools.files import normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service

NAME = normalize(__name__)

system_packages = {Pacman("opensnitch")}
files = [
    UserService(f"{NAME}/opensnitch.service"),
]


@after
def start_opensnitch_services() -> None:
    ensure_service("opensnitchd.service")
    ensure_service("opensnitch.service", user=True)
