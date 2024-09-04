from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.files import XDGConfigFile
from cfgtools.system.systemd import UserService, ensure_service

from wayland.hyprland import NAME

packages = {
    Pacman("hyprpaper"),
}
files = {
    XDGConfigFile(f"{NAME}/hyprpaper.conf", "hypr/hyprpaper.conf"),
    UserService(f"{NAME}/hyprpaper.service", "hyprpaper.service"),
}


@after
def enable_hyprpaper() -> None:
    ensure_service("hyprpaper.service", user=True)
