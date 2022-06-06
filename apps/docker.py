from cfgtools.files import DesktopEntry, UserBin, normalize
from typing import Optional

import docker

NAME = normalize(__name__)


class App:
    def __init__(self, folder: str, name: Optional[str] = None):
        name = name if name else folder
        self.bin = UserBin(f"{NAME}/{folder}/run.sh", name)
        self.entry = DesktopEntry(f"{NAME}/{folder}/entry.desktop", name)
