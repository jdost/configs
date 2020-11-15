from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import hide_xdg_entry

import aur

system_packages={AUR("picom-tryone-git")}
files=[
    XDGConfigFile(f"{__name__}/picom.conf"),
    UserService(f"{__name__}/compositor.service"),
]
unwanted_entries=["compton", "picom"]


@after
def start_compositor_service() -> None:
    ensure_service("compositor", user=True)


@after
def hide_picom_desktop_entries() -> None:
    [hide_xdg_entry(e) for e in unwanted_entries]
