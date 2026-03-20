from gi.repository import Gtk  # type: ignore
from ignis.base_widget import BaseWidget


class LevelBar(Gtk.LevelBar, BaseWidget):
    __gtype_name__ = "IgnisLevelBar"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(self, **kwargs):
        Gtk.LevelBar.__init__(self)
        self.override_enum("mode", Gtk.LevelBarMode)
        BaseWidget.__init__(self, **kwargs)
