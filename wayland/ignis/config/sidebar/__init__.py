from ignis import utils, widgets
from utils.style import add_style

from .widget import SidebarWidget

sidebar: None | "Sidebar" = None


class Sidebar:
    def __init__(self) -> None:
        self.container = widgets.Box(
            css_classes=["sidebar"],
            homogeneous=False,
            vertical=True,
            child=[],
        )
        self.revealer = widgets.Revealer(
            reveal_child=False,
            transition_duration=200,
            transition_type="slide_left",
            child=widgets.Scroll(
                hscrollbar_policy="never",
                vscrollbar_policy="automatic",
                child=self.container,
            ),
        )
        self.window = widgets.Window(
            namespace="ignis.sidebar",
            monitor=0,
            anchor=["top", "right", "bottom"],
            exclusivity="normal",
            css_classes=["sidebar-background"],
            child=self.revealer,
            visible=False,
        )

        self.widgets = [widget() for widget in SidebarWidget._registry]

    def toggle(self, monitor: int | None = None) -> None:
        if not self.window.visible:
            if monitor is not None:
                self.window.monitor = monitor

            self.populate_window()
            self.window.visible = True
            self.revealer.reveal_child = True
            return

        self.revealer.reveal_child = False
        utils.Timeout(ms=self.revealer.transition_duration, target=self._cleanup)

    def _cleanup(self) -> None:
        self.window.visible = False
        for widget in self.widgets:
            widget.destroy()

    def populate_window(self) -> None:
        self.container.child = [widget.render() for widget in self.widgets]

    @classmethod
    def init(cls) -> None:
        add_style(__name__)
        global sidebar
        sidebar = cls()


def sidebar_toggle(monitor: int | None = None) -> None:
    global sidebar
    if sidebar is None:
        return

    sidebar.toggle(monitor)
