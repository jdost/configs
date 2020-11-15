import os
import shutil

from cfgtools.files import EnvironmentFile, File, HOME, XDGConfigFile
from cfgtools.system.arch import AUR, Pacman
from cfgtools.hooks import after

packages = {
    Pacman("zsh"), Pacman("zsh-syntax-highlighting"), Pacman("zsh-completions"),
    AUR("./aur/pkgs/cli-utils"),
}
files = [
    File(f"{__name__}/zshrc", HOME / ".zshrc"),
    XDGConfigFile(f"{__name__}/settings"),
    EnvironmentFile(__name__),
]


@after
def change_user_shell() -> None:
    if os.environ.get("SHELL") == "zsh":
        return

    subprocess.run(["chsh", "-s", shutil.which("zsh")])
