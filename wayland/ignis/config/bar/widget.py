from enum import Flag, auto
from typing import ClassVar

from ignis import widgets
from utils.widgets import BaseWidget


class BarSide(Flag):
    LEFT = auto()
    RIGHT = auto()


class BarMonitor(Flag):
    PRIMARY = auto()
    SECONDARY = auto()
    ALL = PRIMARY | SECONDARY


class BarWidget(BaseWidget):
    side: ClassVar[BarSide] = BarSide.RIGHT
    priority: ClassVar[int] = -1
    monitor: ClassVar[BarMonitor] = BarMonitor.PRIMARY

    def __init__(self, monitor: int) -> None:
        self.monitor_id = monitor

    @classmethod
    def build(cls, monitor: int) -> widgets.Widget:
        return cls(monitor).render()

    @classmethod
    def register(cls) -> None:
        from bar import Bar

        Bar.register_widget(cls)

    @staticmethod
    def sort_key(src) -> tuple[int, str]:
        # Since priority means earlier, we negate it since sort normally wants
        # lower numbers first
        return (-src.priority, src.name)
