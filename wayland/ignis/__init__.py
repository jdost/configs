from typing import Optional

from cfgtools.files import File, InputType, UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after, before
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import UserService, ensure_service
from wayland.hyprland import HyprlandSettings

NAME = normalize(__name__)


class IgnisSettings(File):
    definition: Optional["IgnisSettings"] = None
    loc = XDGConfigFile.DIR / "ignis/settings.json"

    def __init__(self, src: InputType):
        IgnisSettings.definition = self
        super().__init__(src=src, dst=self.loc)


virtualenv = VirtualEnv("ignis", "git+https://github.com/ignis-sh/ignis.git")
packages = {
    Pacman("python-cairo"),
    Pacman("gtk4-layer-shell"),
    AUR("ignis-gvc"),
}
files = {
    XDGConfigFile(f"{NAME}/config", "ignis"),
    UserService(f"{NAME}/ignis.service", "ignis.service"),
    HyprlandSettings(f"{NAME}/hyprland.conf", "ignis"),
    UserBin(virtualenv.location / "bin/ignis", "ignis"),
}


@before
def conditional_deps() -> None:
    """There are some dependencies for specific widgets, so lookup the defined
    widgets and conditionally add them, looks at either an already defined
    settings file or the one about to be linked.
    """
    import json

    widgets = set()
    if IgnisSettings.loc.exists():
        widgets = set(json.loads(IgnisSettings.loc.read_text()).get("widgets", []))
    elif IgnisSettings.definition is not None:
        widgets = set(
            json.loads(IgnisSettings.definition.src.read_text()).get("widgets", [])
        )

    if "audio" in widgets:
        packages.add(Pacman("pipewire-pulse"))
    if "bluetooth" in widgets:
        packages.add(Pacman("gnome-bluetooth-3.0"))
    if "battery" in widgets:
        packages.add(Pacman("upower"))


@after
def enable_ignis() -> None:
    ensure_service("ignis.service", user=True)
