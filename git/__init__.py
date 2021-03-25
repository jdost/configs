from pathlib import Path

from cfgtools.files import UserBin, XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

import homebin

FOLDER = Path(__name__)

packages={
    Pacman("openssh"), Pacman("git"), Pacman("man-db"),
    Apt("git"), Apt("openssh-client")
}
files=[
    XDGConfigFile(f"{__name__}/config"),
    XDGConfigFile(f"{__name__}/ignore"),
    UserBin(FOLDER / "wrapper.sh", "git"),
]
