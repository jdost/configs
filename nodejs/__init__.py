from cfgtools.files import XDGConfigFile, UserBin
from cfgtools.system.arch import Pacman


packages={Pacman("npm")}
files=[
    XDGConfigFile(f"{__name__}/npmrc", "npm/npmrc"),
    UserBin(f"{__name__}/wrapper.sh", "npm"),
]
