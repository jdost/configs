from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.system.nix import NixPkgBin

import vim

packages={
    Pacman("neovim"), Pacman("python-pynvim"),
    NixPkgBin("neovim"),
}
nvim_files = {
    XDGConfigFile("vim/neovim.vim", "nvim/init.vim"),
}
