from pathlib import Path

from cfgtools.files import (XDG_CONFIG_HOME, DesktopEntry, File, UserBin,
                            normalize)
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.utils import xdg_settings_get, xdg_settings_set


class SettingsFile(File):
    DIR = XDG_CONFIG_HOME / "web-xdg-open"

    def __init__(self, src: str, tgt: str):
        super().__init__(src=src, dst=self.DIR / tgt)


NAME = normalize(__name__)
DEFAULT_BROWSER = XDG_CONFIG_HOME / "web-xdg-open/default"

packages = {
    Pacman("xdg-utils"),
}
files = [
    DesktopEntry(f"{NAME}/web-xdg-open.desktop"),
    UserBin(f"{NAME}/web-xdg-open.py", "web-xdg-open"),
]


@after
def register_as_default_browser() -> None:
    # xdg-settings set default-web-browser web-xdg-open.desktop
    tgt = "web-xdg-open.desktop"
    if xdg_settings_get("default-web-browser") != tgt:
        xdg_settings_set("default-web-browser", tgt)


def set_default(browser: str) -> None:
    from shutil import which

    if not DEFAULT_BROWSER.exists():
        @after
        def register_default_browser() -> None:
            target = Path(which(browser))
            DEFAULT_BROWSER.parent.mkdir(parents=True, exist_ok=True)
            # symlink DEFAULT_BROWSER -> target
            DEFAULT_BROWSER.symlink_to(target)
    elif DEFAULT_BROWSER.is_symlink():
        assert DEFAULT_BROWSER.readlink() == Path(which(browser)), (
                "Default web-xdg-open browser already set to: "
                f"{DEFAULT_BROWSER.readlink().name}"
            )
    else:
        raise f"{DEFAULT_BROWSER} should be a symlink"
