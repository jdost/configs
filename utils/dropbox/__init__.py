from cfgtools.files import (HOME, XDG_CONFIG_HOME, InputType,
                            RegisteredFileAction, UserBin, convert_loc,
                            normalize)
from cfgtools.hooks import after
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import UserService, ensure_service
from cfgtools.utils import run

NAME = normalize(__name__)

# NOTE: import the `xorg` or `wayland` submodules to get the correct
# dependencies
# packages = {Pacman("qt5-base")}
virtualenv = VirtualEnv("maestral", "maestral", "maestral-qt")
files = [
    UserBin(virtualenv.location / "bin/maestral", "maestral"),
    UserService(f"{NAME}/dropbox.service"),
]

DROPBOX_DIR = HOME / ".local/dropbox"


class EncryptedFile(RegisteredFileAction):
    """
    Creation Command:
      gpg --encrypt \
          --output <DROPBOX_DIR>/credentials/<src> \
          --recipient <GPG EMAIL> \
          <dst>
    """

    DROPBOX_BASE = DROPBOX_DIR
    U_RO = 0o400

    def __init__(self, src: InputType, dst: InputType):
        self.src = self.DROPBOX_BASE / src
        self.dst = convert_loc(dst)

        super().__init__()

    def dry_run(self) -> None:
        if not self.src.exists():
            raise FileNotFoundError(self.src)

        if self.dst.exists():
            if self.dst.stat().st_mtime > self.src.stat().st_mtime:
                return
        elif not self.dst.parent.exists():
            print(f"$ mkdir {self.dst.parent}")

        print(f"$ gpg --quiet --output {self.dst} --decrypt {self.src}")

    def apply(self) -> None:
        if not self.src.exists():
            raise FileNotFoundError(self.src)

        if self.dst.exists():
            if self.dst.stat().st_mode & 0o777 != self.U_RO:
                self.dst.unlink()
            elif self.dst.stat().st_mtime > self.src.stat().st_mtime:
                return
        elif not self.dst.parent.exists():
            self.dst.parent.mkdir(parents=True)

        print(f"Decrypting: {self.src} -> {self.dst}")
        run(f"gpg --quiet --output {self.dst} --decrypt {self.src}")
        self.dst.chmod(self.U_RO)


# Could be a different `after` hook, but we want to ensure this exists *before*
# potentially starting the service
def setup_initial_config() -> None:
    config_file = XDG_CONFIG_HOME / "maestral/maestral.ini"
    # Don't do anything if it exists, we can look into safely doing this
    # another time
    if config_file.exists():
        return

    config_file.parent.mkdir(parents=True, exist_ok=True)
    DROPBOX_DIR.mkdir(parents=True, exist_ok=True)

    from configparser import ConfigParser

    config = ConfigParser()
    config["sync"] = {"path": str(DROPBOX_DIR)}

    with config_file.open("w") as fp:
        config.write(fp)


@after
def enable_dropbox_service() -> None:
    setup_initial_config()
    ensure_service("dropbox", user=True)
