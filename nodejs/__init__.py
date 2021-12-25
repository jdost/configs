from cfgtools.files import XDGConfigFile, UserBin, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)


packages={Pacman("npm")}
files=[
    XDGConfigFile(f"{NAME}/npmrc", "npm/npmrc"),
    UserBin(f"{NAME}/wrapper.sh", "npm"),
]
