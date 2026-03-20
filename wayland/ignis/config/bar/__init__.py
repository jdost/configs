from typing import ClassVar, Optional

from ignis import utils, widgets
from utils.style import add_style

from bar.icon import BarIconsWidget
from bar.widget import BarMonitor, BarSide, BarWidget


class Bar:
    _widgets: ClassVar[list[type[BarWidget]]] = []

    def __init__(self, monitor_id: int) -> None:
        self.monitor = monitor_id
        self.monitor_mask = (
            BarMonitor.PRIMARY if self.monitor == 0 else BarMonitor.SECONDARY
        )

        self.window = widgets.Window(
            namespace=f"ignis.bar.{monitor_id}",
            monitor=monitor_id,
            css_classes=["bar"],
            anchor=["top", "left", "right"],
            exclusivity="exclusive",
            child=widgets.CenterBox(
                start_widget=self.build_left(),
                end_widget=self.build_right(),
            ),
        )

    def build_left(self) -> Optional[widgets.Box]:
        left_widgets = sorted(
            [
                w
                for w in self._widgets
                if (w.side is BarSide.LEFT and self.monitor_mask & w.monitor)
            ],
            key=BarWidget.sort_key,
        )
        # This is unlikely, but don't show the left bar if nothing to contain
        if not len(left_widgets):
            return None

        return widgets.Box(
            css_classes=["left"],
            child=[widget.build(self.monitor) for widget in left_widgets],
        )

    def build_right(self) -> widgets.Box:
        right_widgets = sorted(
            [
                w
                for w in self._widgets
                if (w.side is BarSide.RIGHT and self.monitor_mask & w.monitor)
            ],
            key=BarWidget.sort_key,
        )
        # This is unlikely, but don't show the right bar if nothing to contain
        if not len(right_widgets):
            return None

        return widgets.Box(
            css_classes=["right"],
            child=[widget.build(self.monitor) for widget in right_widgets],
        )

    @classmethod
    def register_widget(cls, widget: type[BarWidget]) -> None:
        cls._widgets.append(widget)

    @classmethod
    def init(cls) -> None:
        add_style(__name__)
        BarIconsWidget.register()

        for i in range(utils.get_n_monitors()):
            cls(i)
