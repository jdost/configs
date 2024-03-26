from cfgtools.files import XDGConfigFile
from cfgtools.system.arch import AUR

packages={AUR("ttf-fluentui-system-icons")}
files=[
    XDGConfigFile("xorg/polybar/icon_fonts/fluent-config", "polybar/icon-font"),
]
