import re

from ignis import utils, widgets
from ignis.services.notifications import Notification, NotificationAction
from utils.widgets import BaseWidget

from utils import cursor

DEFAULT_ICON = "dialog-information-symbolic"

label_props = {
    "ellipsize",
    "justify",
    "label",
    "max_width_chars",
    "use_markup",
    "wrap",
    "wrap_mode",
    *BaseWidget.__build_props__,
}

MARKDOWN_APPS = {"WebCord"}
MARKDOWN_ELEMENTS = [
    (re.compile("\\*\\*([^\\*]+)\\*\\*"), r"<b>\1</b>"),  # **bold text**
    (
        re.compile("\\[(.+)\\]\\((.+)\\)"),
        r"<u>\1</u>",
    ),  # [a link](to somewhere), we just want the underline for looks
    (re.compile("\\*([^\\*]+)\\*"), r"<i>\1</i>"),  # *italic text*
]


def markdown_to_pango(src: str) -> str:
    res = src.replace("<", "&lt:").replace(">", "&gt;")
    for regex, sub in MARKDOWN_ELEMENTS:
        res = regex.sub(sub, res)

    return res


class Icon(BaseWidget):
    base = widgets.EventBox
    css_classes = ["icon"]
    hexpand = False

    def __init__(self, notification: Notification, *args, **kwargs) -> None:
        self.src = notification
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs) -> widgets.Box:
        if self.src.icon and self.src.icon.startswith("file://"):
            return super().render(
                child=[
                    widgets.Box(
                        css_classes=["image"],
                        style=f'background-image: url("{self.src.icon}");',
                    )
                ],
                *args,
                **kwargs,
            )

        image = DEFAULT_ICON
        if self.src.icon:
            image = self.src.icon
        elif self.src.app_name and utils.get_app_icon_name(self.src.app_name):
            image = self.src.app_name
        elif utils.get_app_icon_name(self.src.app_name):
            image = utils.get_app_icon_name(self.src.app_name)

        return super().render(
            child=[
                widgets.Box(
                    css_classes=["image"],
                    child=[
                        widgets.Icon(
                            halign="start",
                            image=image,
                            pixel_size=34,
                            valign="start",
                        )
                    ],
                )
            ],
            *args,
            **kwargs,
        )


class ActionButton(BaseWidget):
    base = widgets.Button
    css_classes = ["action"]
    cursor = cursor("pointer")
    hexpand = True

    def __init__(self, action: NotificationAction, *args, **kwargs):
        self.src = action
        super().__init__(*args, **kwargs)

    @staticmethod
    def supported(action: NotificationAction) -> bool:
        return action.id != "default"

    def on_click(self, *_) -> None:
        self.src.invoke()

    def render_child(self) -> widgets.Label:
        return widgets.Label(label=self.src.label)


class ActionButtons(BaseWidget):
    base = widgets.Box
    css_classes = ["actions"]

    def __init__(self, actions: list[NotificationAction], *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

    def render_children(self) -> list[widgets.Button]:
        return [
            ActionButton(a).render() for a in self.actions if ActionButton.supported(a)
        ]


class Title(BaseWidget):
    base = widgets.Label
    __build_props__ = label_props
    css_classes = ["summary"]
    ellipsize = "end"
    halign = "start"
    hexpand = True
    justify = "left"
    max_width_chars = 24
    wrap = True
    use_markup = True

    def __init__(self, notification: Notification, *args, **kwargs):
        self.label = notification.summary
        super().__init__(*args, **kwargs)


class BodyText(BaseWidget):
    base = widgets.Label
    __build_props__ = label_props
    css_classes = ["body-text"]
    halign = "start"
    hexpand = True
    justify = "left"
    vexpand = True
    wrap = True
    wrap_mode = "word"
    use_markup = True

    def __init__(self, notification: Notification, *args, **kwargs):
        self.label = (
            markdown_to_pango(notification.body)
            if notification.app_name in MARKDOWN_APPS
            else notification.body
        )
        super().__init__(*args, **kwargs)


class Body(BaseWidget):
    base = widgets.Box
    css_classes = ["text"]
    __build_props__ = {"vertical", *BaseWidget.__build_props__}
    hexpand = True
    vertical = True

    def __init__(self, notification: Notification, *args, **kwargs):
        self.src = notification
        super().__init__(*args, **kwargs)

    def render_children(self) -> list[widgets.Widget]:
        return [
            Title(self.src).render(),
            widgets.Box(
                hexpand=True,
                vexpand=True,
                child=[BodyText(self.src).render()],
            ),
        ]
