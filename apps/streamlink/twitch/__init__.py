from cfgtools.files import XDG_CONFIG_HOME, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import UserService, ensure_service
from cfgtools.utils import hide_xdg_entry
from utils import dropbox

NAME = normalize(__name__)

packages = {AUR("./aur/pkgs/twitch-indicator")}
files = [
    dropbox.EncryptedFile(
        "credentials/twitch.authtoken.gpg",
        XDG_CONFIG_HOME / "twitch-indicator/authtoken",
    ),
    UserService(f"{NAME}/twitch-indicator.service"),
]


@after
def enable_twitch_service() -> None:
    ensure_service("twitch-indicator", user=True)


@after
def hide_unwanted_xdg_entries() -> None:
    hide_xdg_entry("twitch-indicator")
    hide_xdg_entry("twitch-indicator-auth")
