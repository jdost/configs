from cfgtools.hooks import after
from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.utils import hide_xdg_entry

import web_xdg_open

packages={Pacman("mpv"), Pacman("youtube-dl")}
files=[
    XDGConfigFile(f"{__name__}/mpv.conf"),
    web_xdg_open.SettingsFile(f"{__name__}/web-xdg-open", "mpv"),
]


@after
def hide_unwanted_mpv_entries() -> None:
    [hide_xdg_entry(e) for e in ["lstopo", "qvidcap", "qv4l2"]]
