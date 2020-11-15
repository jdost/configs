from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService

packages={Pacman("unclutter")}
files=[
    UserService(f"{__name__}/unclutter.service"),
]


@after
def unclutter_enabled() -> None:
    ensure_service("unclutter", user=True)
