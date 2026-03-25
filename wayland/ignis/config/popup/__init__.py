import settings
from ignis import utils, widgets
from utils.style import add_style

from .window import PopupWindow


class Popup:
    def __init__(self, monitor_id: int) -> None:
        self.window = widgets.Window(
            namespace="ignis.popup",
            monitor=monitor_id,
            css_classes=["popup"],
            anchor=["top", "right"],
            exclusivity="ignore",
            margin_top=settings.font_size * 2,
            visible=False,
        )

        self.handlers: dict[str, PopupWindow] = {}
        self.active_handler: None | PopupWindow = None
        utils.Timeout(ms=500, target=self.setup)

    def setup(self) -> None:
        for handler_builder in PopupWindow._registry:
            handler = handler_builder()
            handler.connect("display", self.display_hook)
            handler.connect("destroyed", self.cleanup)
            self.handlers[handler.name] = handler

    def toggle(self, name: str) -> None:
        if name not in self.handlers:
            print(f"Unknown handler: {name}")
            return None

        self.handlers[name].toggle()

    def cleanup(self, handler: PopupWindow) -> None:
        if handler is not self.active_handler:
            return

        self.window.visible = False

    def display_hook(self, handler: PopupWindow) -> None:
        if self.active_handler and self.active_handler is not handler:
            self.active_handler.destroy()
        if not self.active_handler or self.active_handler is not handler:
            self.active_handler = handler

        self.window.child = self.active_handler.render()
        self.window.visible = True

    @classmethod
    def init(cls) -> None:
        add_style(__name__)
        setattr(cls, "_ref", cls(0))


class PopupMessage:
    def __init__(self):
        pass

    def toggle(self, hook_name: str) -> None:
        if not hasattr(Popup, "_ref"):
            return

        Popup._ref.toggle(hook_name)


popup = PopupMessage()
