from utils.style import add_style

from .bar import AudioIcon
from .osd import VolumeHook


def setup() -> None:
    add_style(__name__)
    AudioIcon.register()
    VolumeHook.register()
