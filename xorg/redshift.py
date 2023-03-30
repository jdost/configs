import dropbox
from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service
from cfgtools.utils import hide_xdg_entry

packages = {Pacman("redshift")}
files = [
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/redshift/redshift.conf",
        "redshift/redshift.conf",
    ),
]


@after
def enable_redshift():
    # The service file provided by the package is set to use `default` as the
    # target, which launches before we have a display manager and crashes, so
    # we need to make a higher precedence copy (in the ~/.config/system folder)
    # and fix the launch target
    # NOTE: users the `UserService` for the path convenience
    user_service_copy = UserService(
        "/usr/lib/systemd/user/redshift-gtk.service", "redshift-gtk"
    )
    if not user_service_copy.dst.exists():
        user_service_copy.dst.write_text(
            user_service_copy.src.read_text().replace(
                "WantedBy=default.target", "WantedBy=xorg.target"
            )
        )
    ensure_service("redshift-gtk", user=True)


@after
def hide_unwanted_xdg_entries() -> None:
    for entry in [
        "geoclue-demo-agent", "geoclue-where-am-i", "redshift-gtk", "redshift"
    ]:
        hide_xdg_entry(entry)
