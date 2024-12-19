from cfgtools.files import (XDG_CONFIG_HOME, File, InputType, XDGConfigFile,
                            normalize)

NAME = normalize(__name__)

class WaylandRC(File):
    folder = XDG_CONFIG_HOME / "wayland/rc.d"
    def __init__(self, src: InputType, name: str, priority: int = 50):
        super().__init__(src=src, dst=WaylandRC.folder / f"{priority:02d}-{name}.sh")

files = {
    File(f"{NAME}/wayland.target", XDG_CONFIG_HOME / "systemd/user/wayland.target"),
    XDGConfigFile(f"{NAME}/rc.sh"),
    WaylandRC(f"{NAME}/qt.waylandrc", "qt", priority=10),
    WaylandRC(f"{NAME}/gtk.waylandrc", "gtk", priority=10),
    # Electron settings to use wayland
    XDGConfigFile(f"{NAME}/electron-flags.conf", "electron-flags.conf"),
}
