import apps.android_messages
import apps.calibre
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
import rofi.wayland
import shells.zsh
import utils.cgroups
import utils.docker
import utils.dropbox.wayland
import utils.icons.papirus
import utils.kubernetes
import utils.scrcpy
import utils.screenshot.wayland
import utils.ssh
#import utils.streamdeck
import utils.tmux
import utils.user_dirs
import utils.wallpaper
import vim
import wayland.ags as ags
import wayland.hyprland as hyprland
from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system import set_default_shell
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service
from cfgtools.utils import hide_xdg_entry

set_default_shell(shells.zsh.BIN)
web_xdg_open.set_default("qutebrowser")
configs = {
    hyprland.HyprlandSettings("systems/hershel/hyprland.conf", "system", priority=90),
    ags.AgsSettings("systems/hershel/ags_settings.json"),
    # The 'system' module for ags is special, it's gitignored and meant to be just whatever
    #  small tweaks I may have for a system, in this case it's a button to move the
    #  notifications between monitors
    XDGConfigFile("systems/hershel/ags_module.js", "ags/modules/system.js"),
}
pkgs = {
    Pacman("darktable"), Pacman("shotwell"), Pacman("luminancehdr"),  # Photography
    Pacman("cifs-utils"),  # SMB mount
    Pacman("imv"),  # Image Viewer
    Pacman("gnome-bluetooth-3.0"), Pacman("bluez-utils"), # Bluetooth
}

@after
def hide_unwanted_xdg_entries() -> None:
    """Try and move these as close to the source as possible, only system specific
    packages should be addressed in here."""
    for entry in [
        "avahi-discover", "bssh", "bvnc", # avahi
        "qv4l2", "qvidcap", # v4l/obs
        "lstopo", # hwloc, transient from darktable
        "electron32",  # electron, transient from webcord
    ]:
        hide_xdg_entry(entry)


@after
def enable_services() -> None:
    """Enable services installed in here."""
    ensure_service("bluetooth")
