from cfgtools.files import EnvironmentFile, XDGConfigFile, normalize
from cfgtools.system.arch import AUR
from cfgtools.system.nix import NixPkgBin

NAME = normalize(__name__)

packages = {AUR("./aur/pkgs/cli-utils"),NixPkgBin("bat")}
files = [
    XDGConfigFile(f"{NAME}/config", "bat/config"),
    EnvironmentFile(NAME, "bat"),
]
