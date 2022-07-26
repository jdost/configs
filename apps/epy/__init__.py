from cfgtools.files import DesktopEntry, XDGConfigFile, normalize
from cfgtools.system.arch import AUR

NAME = normalize(__name__)

system_packages = {
    AUR("epy-git")
}
files = [
    XDGConfigFile(f"{NAME}/configuration.json", "epy/configuration.json"),
    DesktopEntry(f"{NAME}/epy.desktop"),
]
