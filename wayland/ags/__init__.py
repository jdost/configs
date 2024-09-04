from cfgtools.files import XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.systemd import UserService, ensure_service

from wayland.hyprland import HyprlandSettings

NAME = normalize(__name__)

packages = {
    AUR("aylurs-gtk-shell"),
    Pacman("libdbusmenu-gtk3"),
}
files = {
    XDGConfigFile(f"{NAME}/config", "ags"),
    UserService(f"{NAME}/ags.service", "ags.service"),
    HyprlandSettings(f"{NAME}/hyprland.conf", "ags"),
}


@after
def enable_ags() -> None:
    ensure_service("ags.service", user=True)
