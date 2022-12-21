from cfgtools.files import DesktopEntry, UserBin
from pathlib import Path
from typing import Optional

import docker

apps_folder = Path(__file__).parent


class App:
    def __init__(self, folder: str, name: Optional[str] = None):
        name = name if name else folder
        self.bin = UserBin(f"{apps_folder}/{folder}/run.sh", name)
        self.entry = DesktopEntry(f"{apps_folder}/{folder}/entry.desktop", name)
