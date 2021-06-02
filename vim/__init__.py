from pathlib import Path

from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt
from cfgtools.files import EnvironmentFile, UserBin, XDGConfigFile

FOLDER = Path(__file__).parent
CONFIG_FILES = ["vimrc", "ftplugin", "plugin", "plugins.vim"]

packages={Pacman("vim"), Apt("vim")}
files=[
    EnvironmentFile(__name__),
    UserBin(FOLDER / "wrapper.sh", "vim"),
    XDGConfigFile(f"{__name__}/neovim.vim", "nvim/init.vim")
] + [XDGConfigFile(f"{__name__}/{f}") for f in CONFIG_FILES]

