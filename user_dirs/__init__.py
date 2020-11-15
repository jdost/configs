import subprocess

from pathlib import Path

from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service


packages = {Pacman("xdg-user-dirs")}
files = [
    XDGConfigFile("user_dirs/dirs", "user-dirs.dirs")
]


@after
def ensure_user_dirs_exist() -> None:
    with open("user_dirs/dirs", "r") as dirs_file:
        for line in dirs_file:
            if line.startswith("#"):
                continue

            dirname = line.split("=")[1]\
                .strip('"\n')\
                .replace("$HOME", str(Path.home()))

            location = Path(dirname)
            if not location.exists():
                location.mkdir(parents=True)

    # this *can't* run first otherwise it will remove the symlink and replace
    #   with a bad default file
    ensure_service("xdg-user-dirs-update", user=True)
