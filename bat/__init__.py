from cfgtools.files import EnvironmentFile, XDGConfigFile
from cfgtools.system.arch import AUR

packages = {AUR("./aur/pkgs/cli-utils"),}
files = [
    XDGConfigFile(f"{__name__}/config"),
    EnvironmentFile(__name__),
]
