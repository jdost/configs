from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman

packages = {Pacman("sxhkd")}
files = [XDGConfigFile("sxhkd/sxhkdrc")]
