from ignis import widgets
from ignis.gobject import IgnisGObject, IgnisSignal
from utils.widgets import BaseWidget


class OSDHook(BaseWidget, IgnisGObject):
    _registry: list[type["OSDHook"]] = []

    name: str
    timeout: int = 2000
    hook: tuple[IgnisGObject, str | list[str]]

    base = widgets.Box
    spacing = 15

    def __init__(self) -> None:
        IgnisGObject.__init__(self)
        if not hasattr(self, "css_classes"):
            self.css_classes: list[str] = []

        if self.name not in self.css_classes:
            self.css_classes.append(self.name)

        target, props = self.hook
        if isinstance(props, list):
            for prop in props:
                target.connect(prop, self._display)
        else:
            target.connect(props, self._display)

    def _display(self, *_) -> None:
        self.emit("display")

    @IgnisSignal
    def display(self) -> None:
        pass

    def setup(self, widget: widgets.Widget) -> None:
        pass

    @classmethod
    def register(cls) -> None:
        OSDHook._registry.append(cls)
