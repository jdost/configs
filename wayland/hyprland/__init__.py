from pathlib import Path

import wayland.hyprland.hypridle
from cfgtools.files import File, InputType, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from wayland import WaylandRC

NAME = normalize(__name__)


class HyprlandSettings(File):
    config_dir: Path = XDGConfigFile.DIR / "hypr/hyprland.d"
    lua_config_dir: Path = XDGConfigFile.DIR / "hypr/modules"

    def __init__(self, src: InputType, name: str, priority: int = 50):
        if src.endswith(".lua"):
            super().__init__(
                src=src, dst=HyprlandSettings.lua_config_dir / f"{priority}-{name}.lua"
            )
        else:
            super().__init__(
                src=src, dst=HyprlandSettings.config_dir / f"{priority}-{name}.conf"
            )


@after
def build_lua_init_file() -> None:
    contents: list[str] = []

    if not HyprlandSettings.lua_config_dir.is_dir():
        return

    init_file = HyprlandSettings.lua_config_dir / "init.lua"
    for f in sorted(HyprlandSettings.lua_config_dir.iterdir()):
        if f == init_file:
            continue

        if f.is_file():
            contents.append(
                f'require("modules.{str(f.relative_to(HyprlandSettings.lua_config_dir))[:-4]}")'
            )

    init_file.write_text("\n".join(contents))


packages = {
    Pacman("hyprland"),
    Pacman("xdg-desktop-portal-hyprland"),
}
files = {
    XDGConfigFile(f"{NAME}/hyprland.lua", "hypr/hyprland.lua"),
    HyprlandSettings(f"{NAME}/hyprland.workspaces.lua", "workspaces", priority=1),
    HyprlandSettings(f"{NAME}/hyprland.keys.lua", "keys"),
    HyprlandSettings(f"{NAME}/hyprland.sidebars.lua", "sidebars"),
    HyprlandSettings(f"{NAME}/hyprland.animations.lua", "animations", priority=20),
    WaylandRC(f"{NAME}/waylandrc", "hyprland", priority=1),
}
