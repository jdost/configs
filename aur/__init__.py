from cfgtools.files import UserBin
from cfgtools.system.arch import Pacman

import docker
import homebin

packages={Pacman("binutils")}
files=[
    UserBin("aur/aur.py", "aur")
]
