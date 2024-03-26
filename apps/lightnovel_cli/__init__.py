from cfgtools.files import DesktopEntry, XDGConfigFile, normalize
from cfgtools.system.arch import AUR
from utils import dropbox

NAME = normalize(__name__)

system_packages = {
    AUR("lightnovel-cli-git")
}
files = [
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/lightnovel-cli/novels.txt",
        "lightnovel-cli/novels.txt",
    ),
    DesktopEntry(f"{NAME}/lightnovel-cli.desktop"),
]
