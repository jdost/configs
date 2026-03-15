from ignis import widgets

from bar.widget import BarMonitor, BarSide, BarWidget

from .services import time


class ClockWidget(BarWidget):
    side = BarSide.RIGHT
    monitor = BarMonitor.ALL
    priority = -1

    base = widgets.Label
    css_classes = ["clock"]

    def setup(self, widget: widgets.Label) -> None:
        widget.label = time.bind("output")
