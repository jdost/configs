from cfgtools.files import XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {Pacman("sxhkd")}
files = [XDGConfigFile(f"{NAME}/sxhkdrc", "sxhkd/sxhkdrc")]
