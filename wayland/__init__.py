from cfgtools.files import File, XDG_CONFIG_HOME, normalize

NAME = normalize(__name__)

files = {
    File(f"{NAME}/wayland.target", XDG_CONFIG_HOME / "systemd/user/wayland.target"),
}
