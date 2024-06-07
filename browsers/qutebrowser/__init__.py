from cfgtools.files import UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

from utils import dropbox

NAME = normalize(__name__)

packages = {Pacman("qutebrowser"), Pacman("pdfjs"), Pacman("python-adblock")}
files = [
    UserBin(f"{NAME}/wrapper.sh", "qutebrowser"),
    XDGConfigFile(f"{NAME}/config.py", "qutebrowser/config.py"),
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "greasemonkey", "qutebrowser/greasemonkey"
    ),
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/qutebrowser/quickmarks",
        "qutebrowser/quickmarks",
    ),
] + [
    XDGConfigFile(f"{NAME}/{n}.py", f"qutebrowser/modules.d/{n}.py")
    for n in ["conditionals", "hints", "privacy", "theme"]
]
