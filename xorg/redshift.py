import dropbox
from cfgtools.files import XDGConfigFile
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service

packages={Pacman("redshift")}
files=[
    XDGConfigFile(
        dropbox.DROPBOX_DIR / "configs/redshift/redshift.conf",
        "redshift/redshift.conf",
    ),
]

@after
def enable_redshift():
    ensure_service("redshift-gtk", user=True)
