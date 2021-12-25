from cfgtools.hooks import after
from cfgtools.files import XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.utils import hide_xdg_entry

import web_xdg_open

NAME = normalize(__name__)

packages={Pacman("mpv"), Pacman("yt-dlp")}
files=[
    XDGConfigFile(f"{NAME}/mpv.conf"),
    web_xdg_open.SettingsFile(f"{NAME}/web-xdg-open", "mpv"),
]


@after
def hide_unwanted_mpv_entries() -> None:
    [hide_xdg_entry(e) for e in ["lstopo", "qvidcap", "qv4l2"]]
