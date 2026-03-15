from utils.style import add_style

from .bar import SystemTrayWidget


def setup() -> None:
    add_style(__name__)
    SystemTrayWidget.register()
