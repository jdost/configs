from ignis import widgets
from ignis.gobject import IgnisGObject, IgnisSignal
from utils.transitions import SlideUp
from utils.widgets import BaseWidget


class PopupWindow(BaseWidget, IgnisGObject):
    _registry: list[type["PopupWindow"]] = []
    name: str

    base = widgets.Box
    css_classes = ["popup"]
    on_show = SlideUp(500)
    on_hide = SlideUp(1000)

    def __init__(self, *args, **kwargs):
        IgnisGObject.__init__(self)
        super().__init__(*args, **kwargs)

        self.css_classes = [self.name, *self.css_classes]
        self.shown = False

    def show(self) -> None:
        if self.shown:
            return

        self.shown = True
        self.emit("display")

    def close(self) -> None:
        if not self.shown:
            return

        self.shown = False
        self.destroy()

    def toggle(self) -> None:
        if self.shown:
            self.close()
        else:
            self.show()

    @IgnisSignal
    def display(self) -> None:
        pass

    @classmethod
    def register(cls) -> None:
        PopupWindow._registry.append(cls)
