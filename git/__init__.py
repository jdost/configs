from cfgtools.files import UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

import homebin

NAME = normalize(__name__)

packages={
    Pacman("openssh"), Pacman("git"), Pacman("man-db"),
    Apt("git"), Apt("openssh-client")
}
files=[
    XDGConfigFile(f"{NAME}/config"),
    XDGConfigFile(f"{NAME}/ignore"),
    UserBin(f"{NAME}/wrapper.sh", "git"),
]
