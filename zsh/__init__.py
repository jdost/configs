import getpass
import os
import subprocess

from cfgtools.files import EnvironmentFile, File, HOME, XDGConfigFile, normalize
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.nix import NixPkgBin
from cfgtools.system.ubuntu import Apt
from cfgtools.hooks import after

_SUDO_CHSH = False
NAME = normalize(__name__)

packages = {
    Pacman("zsh"), Pacman("zsh-syntax-highlighting"), Pacman("zsh-completions"),
    AUR("./aur/pkgs/cli-utils"),
    Apt("zsh"), Apt("zsh-common"), Apt("zsh-syntax-highlighting"),
    NixPkgBin("exa"), NixPkgBin("ripgrep", "rg"),
    NixPkgBin("colordiff"), NixPkgBin("fzf"),
}
files = [
    File(f"{NAME}/zshrc", HOME / ".zshrc"),
    XDGConfigFile(f"{NAME}/settings"),
    EnvironmentFile(NAME),
]


@after
def change_user_shell() -> None:
    zsh_bin = "/bin/zsh"
    if os.environ.get("SHELL") == zsh_bin:
        return

    if _SUDO_CHSH:
        subprocess.run(["sudo", "chsh", "-s", zsh_bin, getpass.getuser()])
    else:
        subprocess.run(["chsh", "-s", zsh_bin])
