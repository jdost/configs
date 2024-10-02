from cfgtools.files import EnvironmentFile, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.nix import NixPkgBin

NAME = normalize(__name__)
CONFIG_FILES = ["vimrc", "ftplugin", "plugin", "plugins.vim"]

packages={
    Pacman("neovim"), Pacman("python-pynvim"),
    NixPkgBin("neovim"),
}
files=[
    EnvironmentFile(NAME),
    UserBin(f"{NAME}/wrapper.sh", "vim"),
    XDGConfigFile("vim/neovim.vim", "nvim/init.vim"),
] + [XDGConfigFile(f"{NAME}/{f}") for f in CONFIG_FILES]

