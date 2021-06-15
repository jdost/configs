from cfgtools.files import EnvironmentFile, XDGConfigFile
from cfgtools.system.arch import AUR
from cfgtools.system.nix import NixPkgBin

packages = {AUR("./aur/pkgs/cli-utils"),NixPkgBin("bat")}
files = [
    XDGConfigFile(f"{__name__}/config"),
    EnvironmentFile(__name__),
]
