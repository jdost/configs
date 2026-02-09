from cfgtools.files import UserBin, normalize
from cfgtools.system.arch import Pacman
from wayland.hyprland import HyprlandSettings

NAME = normalize(__name__)

pkgs = {Pacman("ydotool")}
files = {
    UserBin(f"{NAME}/daemon.sh", "macro-daemon"),
    UserBin(f"{NAME}/toggle.sh", "toggle-kmacro"),
    HyprlandSettings(f"{NAME}/hyprland.conf", "keyboard-macro"),
}
