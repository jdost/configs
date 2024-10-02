import rofi
import utils.dropbox
from cfgtools.files import HOME, EnvironmentFile, XDGConfigFile, normalize
from cfgtools.system import GitRepository
from cfgtools.system.arch import Pacman

from wayland import WaylandRC

NAME = normalize(__name__)

packages = {
    Pacman("pass"),
    Pacman("yubikey-manager"),
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
    WaylandRC(f"{NAME}/waylandrc", "auth", priority=20),
]
