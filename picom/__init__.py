from cfgtools.files import XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import hide_xdg_entry

import aur

NAME = normalize(__name__)

system_packages={AUR("picom-git")}
files=[
    XDGConfigFile(f"{NAME}/picom.conf"),
    UserService(f"{NAME}/compositor.service"),
]
unwanted_entries=["compton", "picom"]


@after
def start_compositor_service() -> None:
    ensure_service("compositor", user=True)


@after
def hide_picom_desktop_entries() -> None:
    [hide_xdg_entry(e) for e in unwanted_entries]
