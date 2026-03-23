from ignis import widgets
from ignis.services.notifications import (
    Notification,
)
from utils.transitions import SlideDown
from utils.widgets import BaseWidget

from . import ui

URGENCY = {
    -1: "normal",
    0: "low",
    1: "normal",
    2: "critical",
}


class NotificationPopup(BaseWidget):
    base = widgets.EventBox
    __build_props__ = {"vertical", *BaseWidget.__build_props__}

    css_classes = ["notification"]
    hexpand = True
    vertical = True
    vexpand = True
    on_show = SlideDown(350)
    on_hide = SlideDown(500)

    def __init__(self, src: Notification, parent: widgets.Box, *args, **kwargs) -> None:
        self.src = src
        self.parent = parent
        # Copy rather than mutate the class value
        self.css_classes = [URGENCY.get(self.src.urgency, "normal"), *self.css_classes]

        super().__init__(*args, **kwargs)
        self.src.connect("dismissed", lambda _: self.destroy())

    @property
    def supports_actions(self) -> bool:
        return self.src.app_name not in {"WebCord"}

    def on_destroy(self) -> None:
        self.parent.cleanup()

    def on_right_click(self, *_) -> None:
        self.src.dismiss()

    def render_children(self) -> list[widgets.Box]:
        return [
            widgets.Box(
                vexpand=True,
                child=[
                    ui.Icon(self.src).render(),
                    ui.Body(self.src).render(),
                ],
            ),
            ui.ActionButtons(self.src.actions).render()
            if self.supports_actions
            else None,
        ]
