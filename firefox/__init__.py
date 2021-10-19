from cfgtools.files import DesktopEntry
from cfgtools.system.arch import Pacman

import web_xdg_open

packages = {Pacman("firefox")}

files = [
    DesktopEntry(f"{__name__}/private.desktop", "firefox-private.desktop"),
]
