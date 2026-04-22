from cfgtools.files import File, InputType, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import UserService, ensure_service
from wayland.hyprland import HyprlandSettings

NAME = normalize(__name__)


class QuickshellSettings(File):
    definition: "QuickshellSettings" | None = None
    loc = XDGConfigFile.DIR / "quickshell/settings.json"

    def __init__(self, src: InputType):
        QuickshellSettings.definition = self
        super().__init__(src=src, dst=self.loc)


packages = {
    AUR("quickshell-git"),
    # Pacman("quickshell"),  Need git for network manager support
}
files = {
    XDGConfigFile(f"{NAME}/config", "quickshell"),
    UserService(f"{NAME}/quickshell.service", "quickshell.service"),
    HyprlandSettings(f"{NAME}/hyprland.conf", "quickshell"),
}


@after
def enable_quickshell() -> None:
    ensure_service("quickshell.service", user=True)
