from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, normalize
from cfgtools.system.python import VirtualEnv

NAME = normalize(__name__)

virtualenv = VirtualEnv("epy", "epy-reader", "standard-imghdr")

files = [
    UserBin(virtualenv.location / "bin/epy", "epy"),
    XDGConfigFile(f"{NAME}/configuration.json", "epy/configuration.json"),
    DesktopEntry(f"{NAME}/epy.desktop"),
]
