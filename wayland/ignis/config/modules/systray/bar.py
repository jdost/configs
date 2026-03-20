import asyncio

from bar.widget import BarSide, BarWidget
from ignis import widgets
from ignis.services.system_tray import SystemTrayItem, SystemTrayService
from utils.widgets import BaseWidget

system_tray = SystemTrayService.get_default()


class TrayIcon(BaseWidget):
    base = widgets.Button
    __build_props__ = {"tooltip_text", *BaseWidget.__build_props__}

    def __init__(self, src: SystemTrayItem, *args, **kwargs) -> None:
        self.src = src
        self.tooltip_text = self.src.bind("tooltip")
        super().__init__(*args, **kwargs)

    def on_click(self, _) -> None:
        if self.src.item_is_menu and self.src.menu:
            self.src.menu.popup()
        else:
            asyncio.create_task(self.src.activate_async())

    def on_right_click(self, event) -> None:
        if not self.src.item_is_menu and self.src.menu:
            self.src.menu.popup()
        else:
            asyncio.create_task(self.src.secondary_activate_async())

    def render_child(self) -> widgets.Box:
        return widgets.Box(
            child=[
                widgets.Icon(image=self.src.bind("icon"), pixel_size=22),
                self.src.menu,
            ]
        )


class SystemTrayWidget(BarWidget):
    side = BarSide.RIGHT
    priority = 10

    css_classes = ["tray"]
    base = widgets.Box

    def setup(self, box: widgets.Box) -> None:
        system_tray.connect(
            "added", lambda _, icon: box.append(TrayIcon(icon).render())
        )
