from cfgtools.files import DesktopEntry
from cfgtools.system.arch import Pacman

packages = {
    Pacman("firefox"),
    Pacman("firefox-decentraleyes"),
    Pacman("firefox-extension-privacybadger"),
    Pacman("firefox-ublock-origin"),
}

files = [
    DesktopEntry(f"{__name__}/private.desktop", "firefox-private.desktop"),
]
