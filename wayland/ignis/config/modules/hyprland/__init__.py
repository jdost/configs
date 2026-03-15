from utils.style import add_style

from .bar import WorkspacesWidget


def setup() -> None:
    add_style(__name__)
    WorkspacesWidget.register()
