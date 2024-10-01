from cfgtools.files import File, UserBin, XinitRC, DesktopEntry, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import hide_xdg_entry

import apps.mpv

NAME = normalize(__name__)

packages={Pacman("xsecurelock"), Pacman("xss-lock")}
files=[
    UserBin(f"{NAME}/screenlock.sh", "_screenlock"),
    UserBin(f"{NAME}/screenlock_wrapper.sh", "screenlock"),
    UserService(f"{NAME}/screenlock.service"),
    XinitRC(NAME, priority=10),
    File(
        f"{NAME}/saver_mpv-cinemagraph",
        "/usr/lib/xsecurelock/saver_mpv-cinemagraph",
    ),
    DesktopEntry(f"{NAME}/screenlock.desktop"),
]


@after
def enable_screenlock_service() -> None:
    ensure_service("screenlock", user=True)
