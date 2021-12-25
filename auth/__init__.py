from cfgtools.files import EnvironmentFile, XDGConfigFile, HOME, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system import GitRepository

import dropbox
import rofi

NAME = normalize(__name__)

packages = {
    Pacman("pass"),
    Pacman("yubikey-manager"),
    Pacman("xclip"),
    Pacman("xdotool"),
    GitRepository(
        HOME / ".local/dropbox/pass.git",
        HOME / ".local/password_store",
    ),
}
files = [
    XDGConfigFile(f"{NAME}/totp_rofi", "rofi/scripts/totp"),
    XDGConfigFile(f"{NAME}/pass_rofi", "rofi/scripts/pass"),
    XDGConfigFile(f"{NAME}/config.rasi", "rofi/themes/auth.rasi"),
    EnvironmentFile(NAME),
]
