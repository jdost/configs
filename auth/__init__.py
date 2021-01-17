from pathlib import Path

from cfgtools.files import EnvironmentFile, XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.system import GitRepository

import dropbox
import rofi

packages = {
    Pacman("pass"),
    Pacman("yubikey-manager"),
    Pacman("xclip"),
    Pacman("xdotool"),
    GitRepository(
        Path.home() / ".local/dropbox/pass.git",
        Path.home() / ".local/password_store",
    ),
}
files = [
    XDGConfigFile(f"{__name__}/totp_rofi", "rofi/scripts/totp"),
    XDGConfigFile(f"{__name__}/pass_rofi", "rofi/scripts/pass"),
    XDGConfigFile(f"{__name__}/config.rasi", "rofi/themes/auth.rasi"),
    EnvironmentFile(__name__),
]
