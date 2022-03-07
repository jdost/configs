from cfgtools.files import EnvironmentFile, File, Folder, HOME, XinitRC, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service

NAME = normalize(__name__)
USER_GPG_FOLDER = HOME / ".local/gpg"
GPG_CONFIG_FILES = ["gpg.conf", "gpg-agent.conf", "scdaemon.conf"]

packages={Pacman("gnupg"), Pacman("pcsclite"), Pacman("ccid")}
files=[
    EnvironmentFile(NAME),
    Folder(USER_GPG_FOLDER, permissions=0o700),
    XinitRC(NAME, priority=20),
] + [File(f"{NAME}/{f}", USER_GPG_FOLDER / f) for f in GPG_CONFIG_FILES]


@after
def smartcard_daemon_running() -> None:
    ensure_service("pcscd.socket")
