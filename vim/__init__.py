from cfgtools.files import EnvironmentFile, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

NAME = normalize(__name__)
CONFIG_FILES = ["vimrc", "ftplugin", "plugin", "plugins.vim"]

packages={Pacman("vim"), Apt("vim")}
files=[
    EnvironmentFile(NAME),
    UserBin(f"{NAME}/wrapper.sh", "vim"),
] + [XDGConfigFile(f"{NAME}/{f}") for f in CONFIG_FILES]

