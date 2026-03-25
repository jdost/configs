from bar.widget import BarMonitor, BarSide, BarWidget
from ignis import widgets
from sidebar import sidebar_toggle

from utils import cursor

from .services import date, time


class ClockWidget(BarWidget):
    side = BarSide.RIGHT
    monitor = BarMonitor.ALL
    priority = -1

    base = widgets.Button
    css_classes = ["clock"]
    cursor = cursor("pointer")

    def on_click(self, *_) -> None:
        sidebar_toggle(self.monitor_id)

    def render_child(self) -> widgets.Label:
        return widgets.Label(
            label=time.bind("output"),
            tooltip_text=date.bind("output"),
        )
