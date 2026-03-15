from utils.style import add_style

from .bar import AudioIcon


def setup() -> None:
    add_style(__name__)
    AudioIcon.register()
