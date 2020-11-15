from pathlib import Path
from cfgtools.files import HOME, Folder, UserBin, EnvironmentFile

FOLDER = Path(__name__)

files = [
    Folder(HOME / ".local/bin", permissions=0o755),
    EnvironmentFile(__name__),
    UserBin(FOLDER / "settitle.sh", "settitle"),
]
