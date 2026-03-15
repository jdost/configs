from utils.style import add_style

from .bar import ClockWidget


def setup() -> None:
    add_style(__name__)
    ClockWidget.register()
