import asyncio

from ignis import utils, widgets
from ignis.services.notifications import (
    Notification,
    NotificationService,
)
from utils.style import add_style

from utils import monitors

from .popup import NotificationPopup

notifications = NotificationService.get_default()


class Notifications:
    def __init__(self, monitor_id: int) -> None:
        self.monitor = monitor_id
        self.popup_widget = widgets.Box(
            vertical=True,
            child=[],
        )

        self.window = widgets.Window(
            namespace=f"ignis.notifications.{self.monitor}",
            monitor=self.monitor,
            css_classes=["notification-popups"],
            anchor=["top", "right"],
            child=self.popup_widget,
            visible=False,
        )

    async def render_popup(self, notification: Notification) -> None:
        popup = NotificationPopup(notification, self)
        self.window.visible = True
        w = popup.render()
        self.popup_widget.append(w)

    def cleanup(self) -> None:
        if len(self.popup_widget.child) == 0:
            self.window.visible = False

    @classmethod
    def init(cls) -> list["Notifications"]:
        add_style(__name__)

        notification_by_monitor: dict[int, "Notification"] = {}
        for i in range(utils.get_n_monitors()):
            notification_by_monitor[i] = cls(i)

        def route_popup(notification: Notification):
            asyncio.create_task(
                notification_by_monitor[monitors.focused()].render_popup(notification)
            )

        notifications.connect("new_popup", lambda _, notif: route_popup(notif))
        return list(notification_by_monitor.values())
