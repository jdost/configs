from pathlib import Path

from cfgtools.files import File, InputType, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)


class HyprlandSettings(File):
    config_dir: Path = XDGConfigFile.DIR / "hypr/hyprland.d"

    def __init__(self, src: InputType, name: str, priority: int = 50):
        super().__init__(src=src, dst=HyprlandSettings.config_dir / f"{priority}-{name}.conf")


packages = {
    Pacman("hyprland"),
}
files = {
    XDGConfigFile(f"{NAME}/hyprland.conf", "hypr/hyprland.conf"),
    HyprlandSettings(f"{NAME}/hyprland.keys.conf", "keys"),
}