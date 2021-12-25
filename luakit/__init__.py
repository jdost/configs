from cfgtools.files import HOME, UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import run

NAME = normalize(__name__)

packages={Pacman("luakit")}

files=[
    UserBin(f"{NAME}/adblock-update.sh", "_adblock-update"),
    UserService(f"{NAME}/adblock-update.service"),
    UserService(f"{NAME}/adblock-update.timer"),
    XDGConfigFile(f"{NAME}/userconf.lua"),
    XDGConfigFile(f"{NAME}/theme.lua"),
]

@after
def periodic_adblock_updates() -> None:
    ensure_service("adblock-update.timer", user=True)
    if not (HOME / ".local/share/luakit/adblock/easylist.txt").exists():
        run("_update-adblock")
