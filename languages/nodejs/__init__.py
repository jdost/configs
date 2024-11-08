from cfgtools.files import (HOME, EnvironmentFile, Folder, UserBin,
                            XDGConfigFile, normalize)
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
    UserBin(f"{NAME}/wrapper.sh", "npx"),
    Folder(HOME / ".local/nodejs/lib"),
    EnvironmentFile(NAME),
]
