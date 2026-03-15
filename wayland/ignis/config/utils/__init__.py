from pathlib import Path
from typing import Optional

from gi.repository import Gdk
from ignis import widgets


def cursor(name: str) -> Gdk.Cursor:
    return Gdk.Cursor.new_from_name(name)


def toggle_class(widget: widgets.Widget, name: str, add: Optional[bool] = None) -> bool:
    if name in widget.css_classes:
        if add is True:
            return True
        widget.remove_css_class(name)
        return False
    else:
        if add is False:
            return False
        widget.add_css_class(name)
        return True


def config_root() -> Path:
    if hasattr(config_root, "_root"):
        return config_root._root

    loc = Path(__file__)
    while not (loc / "config.py").exists():
        loc = loc.parent

    setattr(config_root, "_root", loc)
    return loc
