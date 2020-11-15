from pathlib import Path

from cfgtools.system.arch import Pacman
from cfgtools.files import XDGConfigFile, EnvironmentFile

FOLDER = Path(__file__).parent
CONFIG_FILES = ["vimrc", "ftplugin", "plugin", "plugins.vim"]

packages={Pacman("vim")}
files=[
    EnvironmentFile(__name__)
] + [XDGConfigFile(f"{__name__}/{f}") for f in CONFIG_FILES]

