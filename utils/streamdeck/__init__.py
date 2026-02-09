from cfgtools.files import normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import UserService, ensure_service

NAME = normalize(__name__)

pkgs = {
    AUR("streamcontroller-git"),
}
files = [
    UserService(f"{NAME}/streamdeck.service"),
]


@after
def enable_streamdeck_service() -> None:
    ensure_service("streamdeck", user=True)
