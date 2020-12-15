from cfgtools.files import DesktopEntry, UserBin, XinitRC
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService


packages = {Pacman("feh"), Pacman("curl"), Pacman("which")}
files = [
    UserBin(f"{__name__}/wallpaper.sh", "wallpaper"),
    UserService(f"{__name__}/wallpaper.service"),
    UserService(f"{__name__}/wallpaper.timer"),
    XinitRC(__name__, priority=90),
    DesktopEntry(f"{__name__}/wallpaper.desktop"),
]


@after
def enable_wallpaper_timer() -> None:
    ensure_service("wallpaper.timer", user=True)
