from cfgtools.files import UserBin
from cfgtools.system.arch import Pacman

import utils.docker
import utils.homebin

packages={Pacman("binutils")}
files=[
    UserBin("aur/aur.py", "aur")
]
