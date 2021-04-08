from pathlib import Path

from cfgtools.files import UserBin, XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import run

packages={Pacman("luakit")}

files=[
    UserBin(f"{__name__}/adblock-update.sh", "_adblock-update"),
    UserService(f"{__name__}/adblock-update.service"),
    UserService(f"{__name__}/adblock-update.timer"),
    XDGConfigFile(f"{__name__}/userconf.lua"),
    XDGConfigFile(f"{__name__}/theme.lua"),
]

@after
def periodic_adblock_updates() -> None:
    ensure_service("adblock-update.timer", user=True)
    if not (Path.home() / ".local/share/luakit/adblock/easylist.txt").exists():
        run("_update-adblock")
