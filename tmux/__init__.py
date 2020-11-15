from pathlib import Path

from cfgtools.system.arch import Pacman
from cfgtools.files import File, HOME

packages={Pacman("tmux")}
files=[
    File(Path(__name__) / "tmux.conf", HOME / ".tmux.conf"),
]
