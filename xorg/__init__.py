from cfgtools.system.arch import Pacman
from cfgtools.files import File, HOME, XDG_CONFIG_HOME, XDGConfigFile

packages={
    Pacman("xorg-xinit"), Pacman("xorg-server"), Pacman("xorg-xmodmap"),
    Pacman("xorg-xrdb"),
}
files=[
    File(f"{__name__}/xorg.target", XDG_CONFIG_HOME / "systemd/user/xorg.target"),
    File(f"{__name__}/xinitrc", HOME / ".xinitrc"),
    XDGConfigFile(f"{__name__}/xinitrc.d/90-systemd"),
    XDGConfigFile(f"{__name__}/xinitrc.d/10-xmodmap"),
    XDGConfigFile(f"{__name__}/xinitrc.d/10-xresources"),
    XDGConfigFile(f"{__name__}/caps-ctrl-swap.xmodmap"),
    XDGConfigFile(f"{__name__}/Xresources"),
]
