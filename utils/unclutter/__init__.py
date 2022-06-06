from cfgtools.hooks import after
from cfgtools.files import normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService

packages={Pacman("unclutter")}
files=[
    UserService(f"{normalize(__name__)}/unclutter.service"),
]


@after
def unclutter_enabled() -> None:
    ensure_service("unclutter", user=True)
