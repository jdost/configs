from cfgtools.files import DesktopEntry, UserBin
from typing import Optional

import docker


class App:
    def __init__(self, folder: str, name: Optional[str] = None):
        name = name if name else folder
        self.bin = UserBin(f"{__name__}/{folder}/run.sh", name)
        self.entry = DesktopEntry(f"{__name__}/{folder}/entry.desktop", name)
