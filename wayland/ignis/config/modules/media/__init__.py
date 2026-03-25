from utils.style import add_style

from .bar import MprisIcon
from .popup import MprisPopup


def setup() -> None:
    add_style(__name__)
    MprisIcon.register()
    MprisPopup.register()
