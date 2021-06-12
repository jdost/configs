import vim

from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt
from cfgtools.files import XDGConfigFile

packages={
    Pacman("neovim"), Pacman("python-pynvim"),
    Apt("neovim"), Apt("python3-neovim"),
}
nvim_files = {
    XDGConfigFile("vim/neovim.vim", "nvim/init.vim"),
}
