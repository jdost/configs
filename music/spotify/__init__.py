from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, normalize
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.systemd import UserService

NAME = normalize(__name__)

pkgs = {
    Pacman("jq"),  # jq is used to keep the username centralized for spotifyd
    Pacman("spotify-player"),
    Pacman("spotifyd"),
}
files = {
    DesktopEntry(f"{NAME}/spotify.desktop"),
    UserBin(f"{NAME}/spotifyd-wrapper.sh", "_spotifyd-wrapper"),
    UserBin(f"{NAME}/spotify-wrapper.sh", "spotify"),
    UserService(f"{NAME}/spotifyd.service"),
    XDGConfigFile(f"{NAME}/spotifyd.conf", "spotifyd/spotifyd.conf"),
    XDGConfigFile(f"{NAME}/spotify-player.toml", "spotify-player/base.toml"),
}
