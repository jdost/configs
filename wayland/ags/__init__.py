from typing import Optional

from cfgtools.files import File, InputType, XDGConfigFile, normalize
from cfgtools.hooks import after, before
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.systemd import UserService, ensure_service
from wayland.hyprland import HyprlandSettings

NAME = normalize(__name__)


class AgsSettings(File):
    definition: Optional['AgsSettings'] = None
    loc = XDGConfigFile.DIR / "ags/settings.json"

    def __init__(self, src: InputType):
        AgsSettings.definition = self
        super().__init__(src=src, dst=self.loc)


packages = {
    AUR("aylurs-gtk-shell"),
    Pacman("libdbusmenu-gtk3"),
}
files = {
    XDGConfigFile(f"{NAME}/config", "ags"),
    UserService(f"{NAME}/ags.service", "ags.service"),
    HyprlandSettings(f"{NAME}/hyprland.conf", "ags"),
}


@before
def conditional_deps() -> None:
    """There are some dependencies for specific widgets, so lookup the defined
    widgets and conditionally add them, looks at either an already defined
    settings file or the one about to be linked.
    """
    import json


    widgets = set()
    if AgsSettings.loc.exists():
        widgets = set(
            json.loads(AgsSettings.loc.read_text()).get("widgets", [])
        )
    elif AgsSettings.definition is not None:
        widgets = set(
            json.loads(AgsSettings.definition.src.read_text()).get("widgets", [])
        )

    if "mpris" in widgets:
        packages.add(Pacman("gvfs"))

@after
def enable_ags() -> None:
    ensure_service("ags.service", user=True)
