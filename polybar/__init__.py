from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import ensure_service, UserService

packages={AUR("polybar"), AUR("./aur/pkgs/ttf-anonymous-pro-ext")}
files=[
    UserService("polybar/statusbar.service"),
    XDGConfigFile(f"{__name__}/config"),
    XDGConfigFile(f"{__name__}/modules"),
]


@after
def enable_statusbar_service() -> None:
    ensure_service("statusbar", user=True)
