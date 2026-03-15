from utils.style import add_style

from .bar import NetworkIcon


def setup() -> None:
    add_style(__name__)
    NetworkIcon.register()
