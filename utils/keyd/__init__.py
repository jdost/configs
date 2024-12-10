from pathlib import Path
from typing import Optional

from cfgtools.files import File, InputType, convert_loc
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service

packages = {
    Pacman("keyd"),
}


class KeydConfig(File):
    BASE = Path("/etc/keyd/")

    def __init__(self, src: InputType, dst: Optional[InputType] = None):
        if dst:
            super().__init__(
                src, self.BASE / (
                    dst if dst.endswith(".conf") else f"{dst}.conf"
                )
            )
        else:
            super().__init__(src, self.BASE / convert_loc(dst).name)


@after
def enable_keyd_service() -> None:
    ensure_service("keyd")
