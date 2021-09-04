from cfgtools.hooks import after
from cfgtools.files import DesktopEntry, File, UserBin, XDG_CONFIG_HOME
from cfgtools.system.arch import Pacman
from cfgtools.utils import xdg_settings_get, xdg_settings_set


class SettingsFile(File):
    def __init__(self, src: str, tgt: str):
        super().__init__(src=src, dst=XDG_CONFIG_HOME / f"web-xdg-open/{tgt}")


packages={
    Pacman("xdg-utils"),
}
files=[
    DesktopEntry(f"{__name__}/web-xdg-open.desktop"),
    UserBin(f"{__name__}/web-xdg-open.py", "web-xdg-open"),
]


@after
def register_as_default_browser():
    # xdg-settings set default-web-browser web-xdg-open.desktop
    tgt = "web-xdg-open.desktop"
    if xdg_settings_get("default-web-browser") != tgt:
        xdg_settings_set("default-web-browser", tgt)
