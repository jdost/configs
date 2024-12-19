from cfgtools.files import UserBin, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {Pacman("playerctl")}
files = {
    UserBin(f"{NAME}/playerctl-wrapper.sh", "playerctl"),
}
