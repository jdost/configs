from cfgtools.files import UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

import utils.homebin

NAME = normalize(__name__)

packages={
    Pacman("openssh"), Pacman("git"), Pacman("man-db"), Pacman("git-delta"),
    Apt("git"), Apt("openssh-client")
}
files=[
    XDGConfigFile(f"{NAME}/config"),
    XDGConfigFile(f"{NAME}/ignore"),
    UserBin(f"{NAME}/wrapper.sh", "git"),
    UserBin(f"{NAME}/git-rgrep.sh", "git-rgrep"),
]
