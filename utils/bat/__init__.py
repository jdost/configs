from cfgtools.files import EnvironmentFile, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import AUR
from cfgtools.system.nix import NixPkgBin

NAME = normalize(__name__)

packages = {AUR("./aur/pkgs/cli-utils"),NixPkgBin("bat")}
files = [
    XDGConfigFile(f"{NAME}/config", "bat/config"),
    EnvironmentFile(NAME, "bat"),
    UserBin(f"{NAME}/man-wrapper.sh", "man"),
]
