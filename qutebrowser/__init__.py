from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman

packages={Pacman("qutebrowser")}
files=[
    XDGConfigFile(f"{__name__}/config.py", "qutebrowser/config.py"),
]
