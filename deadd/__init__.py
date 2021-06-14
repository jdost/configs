from cfgtools.files import DesktopEntry, XDGConfigFile, UserBin
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import hide_xdg_entry

packages={AUR("deadd-notification-center-bin")}
files=[
    XDGConfigFile(f"{__name__}/deadd.conf"),
    UserService(f"{__name__}/notifications.service"),
    UserBin(f"{__name__}/toggle-notifications.sh", "notifications-toggle"),
    DesktopEntry(f"{__name__}/notifications-toggle.desktop"),
]


@after
def start_notification_service() -> None:
    ensure_service("notifications", user=True)


@after
def cleanup_unwanted_avahi_entries() -> None:
    [hide_xdg_entry(e) for e in ["avahi-discover", "bvnc", "bssh"]]
