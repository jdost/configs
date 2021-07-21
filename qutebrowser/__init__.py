from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman

import dropbox

packages={Pacman("qutebrowser"), Pacman("pdfjs"), Pacman("python-adblock")}
files=[
    XDGConfigFile(f"{__name__}/config.py", "qutebrowser/config.py"),
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "greasemonkey", "qutebrowser/greasemonkey"
    ),
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/qutebrowser/quickmarks",
        "qutebrowser/quickmarks",
    ),
] + [
    XDGConfigFile(f"{__name__}/{n}.py", f"qutebrowser/modules.d/{n}.py")
    for n in ["conditionals", "hints", "privacy", "theme"]
]
