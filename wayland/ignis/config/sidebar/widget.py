from ignis import widgets
from utils.widgets import BaseWidget


class SidebarWidget(BaseWidget):
    _registry: list[type["SidebarWidget"]] = []
    name: str
    priority: int = 0

    base = widgets.CenterBox
    css_classes = ["sidebar-widget"]

    def __init__(self, *args, **kwargs):
        self.css_classes = [self.name, *SidebarWidget.css_classes]
        super().__init__(*args, **kwargs)

    @classmethod
    def register(cls) -> None:
        SidebarWidget._registry.append(cls)
