from cfgtools.files import XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import hide_xdg_entry

import aur

NAME = normalize(__name__)

system_packages={Pacman("picom")}
files=[
    XDGConfigFile(f"{NAME}/picom.conf"),
    UserService(f"{NAME}/picom.service"),
]
unwanted_entries=["compton", "picom"]


@after
def start_compositor_service() -> None:
    ensure_service("picom", user=True)


@after
def hide_picom_desktop_entries() -> None:
    [hide_xdg_entry(e) for e in unwanted_entries]
