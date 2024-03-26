from cfgtools.files import (HOME, EnvironmentFile, UserBin, XDGConfigFile,
                            normalize)
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

NAME = normalize(__name__)

packages={Pacman("tmux"), Apt("tmux")}
files=[
    XDGConfigFile(f"{NAME}/tmux.conf", "tmux/tmux.conf"),
    EnvironmentFile(NAME),
    UserBin(f"{NAME}/wrapper.sh", "tmux")
]
