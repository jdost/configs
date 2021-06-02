from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman

import dropbox

packages={Pacman("qutebrowser")}
files=[
    XDGConfigFile(f"{__name__}/config.py", "qutebrowser/config.py"),
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "greasemonkey", "qutebrowser/greasemonkey"
    ),
]
