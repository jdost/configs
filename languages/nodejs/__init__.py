from cfgtools.files import Folder, HOME, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.node import NodePackage

NAME = normalize(__name__)


packages={
    Pacman("npm"),
    NodePackage("typescript-language-server"),
    NodePackage("eslint"),
    NodePackage("@eslint/js"),
    NodePackage("prettier"),
}
files=[
    XDGConfigFile(f"{NAME}/npmrc", "npm/npmrc"),
    UserBin(f"{NAME}/wrapper.sh", "npm"),
    Folder(HOME / ".local/nodejs/lib"),
]
