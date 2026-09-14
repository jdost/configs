import utils.docker
import utils.homebin
from cfgtools.files import (
    XDG_CONFIG_HOME,
    DesktopEntry,
    UserBin,
    XDGConfigFile,
    normalize,
)
from utils.dropbox import EncryptedFile

NAME = normalize(__name__)

files = {
    XDGConfigFile(f"{NAME}/config.toml", "elia/config.toml"),
    UserBin(f"{NAME}/wrapper.sh", "elia"),
    DesktopEntry(f"{NAME}/elia.desktop"),
    EncryptedFile("credentials/elia.env.gpg", XDG_CONFIG_HOME / "elia/keys.env"),
}
