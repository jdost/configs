import docker

import utils.homebin
from cfgtools.files import UserBin, XDGConfigFile, normalize

NAME = normalize(__name__)

files = {
    XDGConfigFile(f"{NAME}/skills", "claude/skills"),
    UserBin(f"{NAME}/wrapper.sh", "claude"),
}
