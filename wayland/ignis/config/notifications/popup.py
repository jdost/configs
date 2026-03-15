from ignis import widgets
from ignis.services.notifications import (
    Notification,
)

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

    def __init__(self, src: Notification, parent: widgets.Box, *args, **kwargs) -> None:
        self.src = src
        self.parent = parent
        if self.src.urgency in URGENCY:
            self.css_classes.append(URGENCY[self.src.urgency])

        self.src.connect("dismissed", lambda _: self.destroy())
        super().__init__(*args, **kwargs)

    @property
    def supports_actions(self) -> bool:
        return self.src.app_name not in {"WebCord"}

    def destroy(self) -> None:
        self.widget.unparent()
        self.parent.cleanup()

    def on_right_click(self, *_) -> None:
        self.src.dismiss()

    def render_child(self) -> widgets.Box:
        return widgets.Box(
            vexpand=True,
            child=[
                ui.Icon(self.src).render(),
                ui.Body(self.src).render(),
                ui.ActionButtons(self.src.actions).render()
                if self.supports_actions
                else None,
            ],
        )
