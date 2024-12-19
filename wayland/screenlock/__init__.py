from cfgtools.files import DesktopEntry, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from wayland.hyprland.hypridle import HypridleConfig

NAME = normalize(__name__)

packages = {
    Pacman("hyprlock"),
}

files = {
    HypridleConfig(f"{NAME}/hypridle.conf"),
    XDGConfigFile(f"{NAME}/hyprlock.conf", "hypr/hyprlock.conf"),
    DesktopEntry(f"{NAME}/screenlock.desktop"),
}
