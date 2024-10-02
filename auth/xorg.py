import rofi.xorg
from cfgtools.files import XinitRC
from cfgtools.system.arch import Pacman

packages = {
    Pacman("xclip"),
    Pacman("xdotool"),
}
files = {
    XinitRC(NAME, priority=20),
}
