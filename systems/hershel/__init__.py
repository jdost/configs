import apps.android_messages
import apps.calibre
import apps.mpv
import apps.obsidian
import apps.streamlink
import apps.wezterm
import apps.zathura
import aur
import auth.wayland
import browsers.firefox
import browsers.qutebrowser
import browsers.web_xdg_open as web_xdg_open
import git
import gpg
import languages.nodejs
import languages.python
import music.spotify
import rofi
import shells.zsh
import utils.cal
import utils.cgroups
import utils.docker
import utils.dropbox.wayland
import utils.icons.papirus
import utils.kubernetes
import utils.scrcpy
import utils.screenshot.wayland
import utils.ssh

# import utils.streamdeck
import utils.tmux
import utils.user_dirs
import utils.wallpaper
import vim
import wayland.hyprland as hyprland
import wayland.quickshell as quickshell
import wayland.wpaperd
from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system import set_default_shell
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service
from cfgtools.utils import hide_xdg_entry

set_default_shell(shells.zsh.BIN)
web_xdg_open.set_default("qutebrowser")

kasa_venv = VirtualEnv("kasa", "python-kasa")

configs = {
    hyprland.HyprlandSettings("systems/hershel/hyprland.lua", "system", priority=90),
    quickshell.QuickshellSettings("systems/hershel/quickshell_settings.json"),
}
pkgs = {
    # Photography
    Pacman("darktable"),
    Pacman("shotwell"),
    Pacman("luminancehdr"),
    # SMB mount
    Pacman("cifs-utils"),
    # Image Viewer
    Pacman("imv"),
    # Bluetooth
    Pacman("gnome-bluetooth-3.0"),
    Pacman("bluez-utils"),
}


@after
def hide_unwanted_xdg_entries() -> None:
    """Try and move these as close to the source as possible, only system specific
    packages should be addressed in here."""
    for entry in [
        # avahi
        "avahi-discover",
        "bssh",
        "bvnc",
        "qv4l2",
        # v4l/obs
        "qvidcap",
        # hwloc, transient from darktable
        "lstopo",
        # gmic, transient from darktable
        "gmic_qt",
        # electron, transient from webcord
        "electron35",
    ]:
        hide_xdg_entry(entry)


@after
def enable_services() -> None:
    """Enable services installed in here."""
    ensure_service("bluetooth")
