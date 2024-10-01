from cfgtools.files import InputType, XDGConfigFile, normalize
from cfgtools.hooks import after, before
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service

NAME = normalize(__name__)

packages = {
    Pacman("hypridle"),
}

files = {
    UserService(f"{NAME}/hypridle.service", "hypridle.service"),
}


class HypridleConfig(XDGConfigFile):
    DST = "hypr/hypridle.conf"
    num_defined = 0

    def __init__(self, src: InputType):
        HypridleConfig.num_defined += 1
        super().__init__(src, self.DST)


@before
def ensure_configured() -> None:
    if HypridleConfig.num_defined == 0:
        HypridleConfig(f"{NAME}/default.conf")


@after
def enable_hypridle() -> None:
    ensure_service("hypridle.service", user=True)
