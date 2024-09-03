from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService
from utils import dropbox

packages = {
    Pacman("gammastep"), Pacman("libappindicator-gtk3"),
}
files = [
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/gammastep/config.ini",
        "gammastep/config.ini",
    ),
    # Enable the gammastep-indicator to the user wayland target
    UserService(
        "/usr/lib/systemd/user/gammastep-indicator.service",
        "wayland.target.wants/gammastep-indicator.service"
    )
]
