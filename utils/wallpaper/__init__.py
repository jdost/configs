from cfgtools.files import DesktopEntry, UserBin, XinitRC, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService

NAME = normalize(__name__)

packages = {Pacman("curl"), Pacman("which")}
files = [
    UserBin(f"{NAME}/wallpaper.py", "wallpaper"),
    UserService(f"{NAME}/wallpaper.service"),
    UserService(f"{NAME}/wallpaper.timer"),
    XinitRC(NAME, priority=90),
    DesktopEntry(f"{NAME}/wallpaper.desktop"),
]


@after
def enable_wallpaper_timer() -> None:
    ensure_service("wallpaper.timer", user=True)
