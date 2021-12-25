from cfgtools.system.arch import Pacman
from cfgtools.files import File, HOME, XDG_CONFIG_HOME, XDGConfigFile, normalize

NAME = normalize(__name__)

packages={
    Pacman("xorg-xinit"), Pacman("xorg-server"), Pacman("xorg-xmodmap"),
    Pacman("xorg-xrdb"),
}
files=[
    File(f"{NAME}/xorg.target", XDG_CONFIG_HOME / "systemd/user/xorg.target"),
    File(f"{NAME}/xinitrc", HOME / ".xinitrc"),
    XDGConfigFile(f"{NAME}/xinitrc.d/90-systemd"),
    XDGConfigFile(f"{NAME}/xinitrc.d/10-xmodmap"),
    XDGConfigFile(f"{NAME}/xinitrc.d/10-xresources"),
    XDGConfigFile(f"{NAME}/caps-ctrl-swap.xmodmap"),
    XDGConfigFile(f"{NAME}/Xresources"),
]
