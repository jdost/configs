from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman

packages={Pacman("python")}
files=[
    XDGConfigFile(f"{__name__}/pip.conf", "pip/pip.conf"),
]
