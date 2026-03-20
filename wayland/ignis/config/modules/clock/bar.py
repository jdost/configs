from bar.widget import BarMonitor, BarSide, BarWidget
from ignis import widgets

from .services import date, time


class ClockWidget(BarWidget):
    side = BarSide.RIGHT
    monitor = BarMonitor.ALL
    priority = -1

    base = widgets.Label
    css_classes = ["clock"]

    def setup(self, widget: widgets.Label) -> None:
        widget.label = time.bind("output")
        widget.tooltip_text = date.bind("output")
