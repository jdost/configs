from cfgtools.hooks import after
from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.utils import hide_xdg_entry

packages={Pacman("mpv")}
files=[
    XDGConfigFile(f"{__name__}/mpv.conf"),
]


@after
def hide_unwanted_mpv_entries() -> None:
    [hide_xdg_entry(e) for e in ["lstopo", "qvidcap", "qv4l2"]]
