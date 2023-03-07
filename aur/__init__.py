from cfgtools.files import UserBin
from cfgtools.system.arch import Pacman

import homebin
import utils.docker

packages={Pacman("binutils")}
files=[
    UserBin("aur/aur.py", "aur")
]
