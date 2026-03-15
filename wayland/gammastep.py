from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService
from cfgtools.utils import hide_xdg_entry
from utils import dropbox

packages = {
    Pacman("gammastep"),
    Pacman("libappindicator-gtk3"),
    Pacman("gtk3"),
    Pacman("python-gobject"),  # For systray icon
}
files = [
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/gammastep/config.ini",
        "gammastep/config.ini",
    ),
    # Enable the gammastep-indicator to the user wayland target
    UserService(
        "/usr/lib/systemd/user/gammastep-indicator.service",
        "wayland.target.wants/gammastep-indicator.service",
    ),
]


@after
def hide_unwanted_xdg_entries() -> None:
    hide_xdg_entry("gammastep-indicator")
