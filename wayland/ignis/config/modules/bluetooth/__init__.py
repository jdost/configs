from utils.style import add_style

from .bar import BluetoothIcon


def setup() -> None:
    add_style(__name__)
    BluetoothIcon.register()
