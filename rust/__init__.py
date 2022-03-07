from cfgtools.files import EnvironmentFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.nix import NixPkgBin

NAME = normalize(__name__)

pkgs = {Pacman("rust"), Pacman("rust-analyzer"), NixPkgBin("rust-analyzer")}
files = [
    EnvironmentFile(NAME),
]
