import utils.bat
from cfgtools.files import (HOME, EnvironmentFile, File, XDGConfigFile,
                            UserProfile, normalize)
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.nix import NixPkgBin
from cfgtools.system.ubuntu import Apt

NAME = normalize(__name__)
BIN = "/bin/zsh"

packages = {
    Pacman("zsh"), Pacman("zsh-syntax-highlighting"), Pacman("zsh-completions"),
    AUR("./aur/pkgs/cli-utils"),
    Apt("zsh"), Apt("zsh-common"), Apt("zsh-syntax-highlighting"),
    NixPkgBin("exa"), NixPkgBin("ripgrep", "rg"),
    NixPkgBin("colordiff"), NixPkgBin("fzf"),
}
files = [
    File(f"{NAME}/zshrc", HOME / ".zshrc"),
    File(f"{NAME}/zshenv", HOME / ".zshenv"),
    XDGConfigFile(f"{NAME}/settings", "zsh/settings"),
    EnvironmentFile(NAME, "zsh"),
    UserProfile(NAME, "zsh"),
]
