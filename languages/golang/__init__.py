from cfgtools.files import EnvironmentFile, UserBin, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

pkgs = {
    Pacman("go"), Pacman("gopls"),
}

files = {
    UserBin(f"{NAME}/wrapper.sh", "go"),
    EnvironmentFile(NAME),
}
