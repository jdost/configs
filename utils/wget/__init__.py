from cfgtools.files import (UserBin, XDGConfigFile, normalize)
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages={
    Pacman("wget"),
}
files=[
    XDGConfigFile(f"{NAME}/wgetrc", "wgetrc"),
    UserBin(f"{NAME}/wrapper.sh", "wget"),
]
