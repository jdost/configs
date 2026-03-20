import settings
from ignis import utils, widgets
from utils.style import add_style


class Accent:
    def __init__(self, monitor_id: int) -> None:
        self.window = widgets.Window(
            namespace=f"ignis.accent.{monitor_id}",
            layer="bottom",
            monitor=monitor_id,
            css_classes=["accent"],
            exclusivity="ignore",
            anchor=["top", "left", "right"],
            child=widgets.CenterBox(center_widget=widgets.Box()),
        )

    @classmethod
    def init(cls) -> None:
        if not settings.accent:
            return

        add_style(__name__)
        for i in range(utils.get_n_monitors()):
            cls(i)
