from pathlib import Path

from cfgtools.files import (XDG_CONFIG_HOME, DesktopEntry, XDGConfigFile,
                            normalize)
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Deb
from cfgtools.utils import run
from utils.dropbox import EncryptedFile

NAME = normalize(__name__)

packages={
    Pacman("github-cli"),
    Deb("gh", (
        "https://github.com/cli/cli/releases/download/"
        "v2.25.1/gh_2.25.1_linux_amd64.deb"
    )),
}
files=[
    DesktopEntry(f"{NAME}/gh-dash.desktop"),
    XDGConfigFile(f"{NAME}/config.yml", "gh/config.yml"),
    EncryptedFile(
        "credentials/gh.yml.gpg",
        XDG_CONFIG_HOME / "gh/hosts.yml",
    ),
]


@after
def install_gh_extensions() -> None:
    extensions_dir = Path.home() / ".local/share/gh/extensions"

    if not (extensions_dir / "gh-dash").exists():
        # Install the dash extension
        run("gh extension install dlvhdr/gh-dash")
