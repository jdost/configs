import apps.mpv
import apps.obsidian
import apps.wezterm
import apps.zathura
import aur
import auth.wayland
import browsers.firefox
import browsers.qutebrowser
import browsers.web_xdg_open as web_xdg_open
import git
import gpg
import languages.python
import rofi
import rofi.wayland
import shells.zsh
import utils.cal
import utils.cgroups
import utils.diskmgr
import utils.docker
import utils.dropbox.wayland
import utils.icons.papirus
import utils.keyd as keyd
import utils.kubernetes
import utils.screenshot.wayland
import utils.ssh
import utils.tmux
import utils.user_dirs
import utils.wallpaper
import vim
import wayland.ags as ags
import wayland.gammastep
import wayland.hyprland as hyprland
import wayland.hyprland.hyprpaper
import wayland.screenlock
from cfgtools.hooks import after
from cfgtools.system import set_default_shell
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service
from cfgtools.utils import hide_xdg_entry

set_default_shell(shells.zsh.BIN)
web_xdg_open.set_default("qutebrowser")

pkgs = {
    Pacman("iwd"), Pacman("networkmanager"),  # Networking
    Pacman("gnome-bluetooth-3.0"), Pacman("bluez-utils"),  # Bluetooth
    Pacman("brightnessctl"), Pacman("pulsemixer"),  # Media Key helpers
}

configs = {
    hyprland.HyprlandSettings("systems/anthony/hyprland.conf", "system", priority=90),
    ags.AgsSettings("systems/anthony/ags_settings.json"),
    keyd.KeydConfig("systems/anthony/keyd.conf", "main"),
    rofi.RofiModule("systems/anthony/rofi.rasi", "system"),
}

#File("systems/anthony/polybar", XDG_CONFIG_HOME / "polybar/system")
#File("systems/anthony/chromium-flags.conf", XDG_CONFIG_HOME / "chromium-flags.conf")
#XinitRC("systems/anthony", priority=40)
#File("systems/anthony/drirc", HOME / ".drirc")

@after
def hide_unwanted_xdg_entries() -> None:
    """Try and move these as close to the source as possible, but sometimes it's
    tough to keep up when things shift."""
    for entry in [
        "avahi-discover", "bssh", "bvnc", # avahi, this gets added by few things
        "electron32", # electron, downtree from webcord
    ]:
        hide_xdg_entry(entry)

@after
def enable_services() -> None:
    """Enable services installed in here."""
    ensure_service("bluetooth")
    ensure_service("NetworkManager")
    ensure_service("iwd")
    ensure_service("pipewire-pulse.socket", user=True)
