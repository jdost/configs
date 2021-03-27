from pathlib import Path

from cfgtools.files import EnvironmentFile, File, HOME, UserBin
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

packages={Pacman("tmux"), Apt("tmux")}
files=[
    File(Path(__name__) / "tmux.conf", HOME / ".tmux.conf"),
    EnvironmentFile(__name__),
    UserBin("tmux/wrapper.sh", "tmux")
]
