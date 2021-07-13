from cfgtools.files import File, UserBin, XinitRC, DesktopEntry
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import hide_xdg_entry

import mpv

packages={Pacman("xsecurelock"), Pacman("xss-lock")}
files=[
    UserBin(f"{__name__}/screenlock.sh", "_screenlock"),
    UserBin(f"{__name__}/screenlock_wrapper.sh", "screenlock"),
    UserService(f"{__name__}/screenlock.service"),
    XinitRC(__name__, priority=10),
    File(
        f"{__name__}/saver_mpv-cinemagraph",
        "/usr/lib/xsecurelock/saver_mpv-cinemagraph",
    ),
    DesktopEntry(f"{__name__}/screenlock.desktop"),
]


@after
def enable_screenlock_service() -> None:
    ensure_service("screenlock", user=True)
