from pathlib import Path

import wayland.hyprland.hypridle
from cfgtools.files import File, InputType, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from wayland import WaylandRC

NAME = normalize(__name__)


class HyprlandSettings(File):
    config_dir: Path = XDGConfigFile.DIR / "hypr/hyprland.d"

    def __init__(self, src: InputType, name: str, priority: int = 50):
        super().__init__(src=src, dst=HyprlandSettings.config_dir / f"{priority}-{name}.conf")


packages = {
    Pacman("hyprland"), Pacman("xdg-desktop-portal-hyprland"),
}
files = {
    XDGConfigFile(f"{NAME}/hyprland.conf", "hypr/hyprland.conf"),
    HyprlandSettings(f"{NAME}/hyprland.keys.conf", "keys"),
    HyprlandSettings(f"{NAME}/hyprland.sidebars.conf", "sidebars"),
    HyprlandSettings(f"{NAME}/hyprland.animations.conf", "animations"),
    WaylandRC(f"{NAME}/waylandrc", "hyprland", priority=1),
    XDGConfigFile(f"{NAME}/toggle-sidebar.sh", "hypr/toggle-sidebar"),
    XDGConfigFile(f"{NAME}/hyprland-workspace.sh", "hypr/hyprland-workspace"),
}
