import subprocess
from pathlib import Path

from cfgtools.files import RegisteredFileAction, UserBin, convert_loc
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService
from cfgtools.utils import run

packages = {Pacman("qt5-base")}
virtualenv = VirtualEnv("maestral", "maestral", "maestral-qt")
files = [
    UserBin(virtualenv.location / "bin/maestral", "maestral"),
    UserService(f"{__name__}/dropbox.service"),
]


class EncryptedFile(RegisteredFileAction):
    DROPBOX_BASE = Path.home() / ".local/dropbox"
    U_RO=0o400

    def __init__(self, src: str, dst: str):
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

        print(f"$ gpg --output {self.dst} --decrypt {self.src}")

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
        subprocess.run(["gpg", "--output", str(self.dst), "--decrypt", str(self.src)])
        self.dst.chmod(self.U_RO)


@after
def enable_dropbox_service() -> None:
    ensure_service("dropbox", user=True)
