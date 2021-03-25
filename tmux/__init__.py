from pathlib import Path

from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt
from cfgtools.files import File, HOME, UserBin

packages={Pacman("tmux"), Apt("tmux")}
files=[
    File(Path(__name__) / "tmux.conf", HOME / ".tmux.conf"),
    UserBin("tmux/wrapper.sh", "tmux")
]
