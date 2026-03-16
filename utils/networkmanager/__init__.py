from cfgtools.files import DesktopEntry, normalize
from cfgtools.system.arch import Pacman
from wayland.hyprland import HyprlandSettings

NAME = normalize(__name__)

system_packages = {Pacman("networkmanager")}
files = [
    DesktopEntry(f"{NAME}/networkmanager.desktop"),
    HyprlandSettings(f"{NAME}/hyprland.conf", "nmtui"),
]
