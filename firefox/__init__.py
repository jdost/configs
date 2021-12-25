from cfgtools.files import DesktopEntry, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {
    Pacman("firefox"),
    Pacman("firefox-decentraleyes"),
    Pacman("firefox-extension-privacybadger"),
    Pacman("firefox-ublock-origin"),
}
files = [
    DesktopEntry(f"{NAME}/private.desktop", "firefox-private.desktop"),
]
