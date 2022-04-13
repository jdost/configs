from pathlib import Path

from cfgtools.files import DesktopEntry, File, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)

packages = {
    Pacman("firefox"),
    Pacman("firefox-decentraleyes"),
    Pacman("firefox-extension-privacybadger"),
    Pacman("firefox-ublock-origin"),
}
files = [
    DesktopEntry(f"{NAME}/private.desktop", "firefox-private.desktop"),
]


@after
def symlink_firefox_profile_userjs() -> None:
    profile = None
    for setting in (Path.home() / ".mozilla/firefox").glob("*"):
        if not setting.is_dir():
            continue
        # This is kind of hacky, the profile looks something like:
        #   NNNNNNNN.<name>
        # so we try and pattern match this with 8 characters followed by a dot
        parts = setting.name.split(".", 2)
        if not len(parts) == 2:
            continue
        if len(parts[0]) == 8:
            # Uses the same underlying handler, just manually applies it
            user_js = File(f"{__name__}/user.js", setting / "user.js")
            user_js.apply()
