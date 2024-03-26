from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import AUR

packages={AUR("ttf-material-design-icons-git")}
files=[
    XDGConfigFile("xorg/polybar/icon_fonts/material-config", "polybar/icon-font"),
]
