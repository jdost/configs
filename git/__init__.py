from pathlib import Path

from cfgtools.files import UserBin, XDGConfigFile
from cfgtools.system.arch import Pacman

import homebin

FOLDER = Path(__name__)

packages={Pacman("openssh"), Pacman("git"), Pacman("man-db")}
files=[
    XDGConfigFile(f"{__name__}/config"),
    XDGConfigFile(f"{__name__}/ignore"),
    UserBin(FOLDER / "wrapper.sh", "git"),
]
