import rofi
import utils.dropbox
from cfgtools.files import (HOME, EnvironmentFile, XDGConfigFile, XinitRC,
                            normalize)
from cfgtools.system import GitRepository
from cfgtools.system.arch import Pacman

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
    XinitRC(NAME, priority=20),
    EnvironmentFile(NAME),
]
