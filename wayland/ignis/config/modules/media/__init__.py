from utils.style import add_style

from .bar import MprisIcon


def setup() -> None:
    add_style(__name__)
    MprisIcon.register()
