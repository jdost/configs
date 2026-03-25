import asyncio

from ignis import widgets
from ignis.gobject import Binding
from ignis.services.mpris import MprisService
from utils.widgets import BaseWidget

from utils import cursor


class CoverArt(BaseWidget):
    base = widgets.Box
    css_classes = ["cover-art"]
    valign = "start"

    def __init__(self, art_url: Binding, *args, **kwargs):
        self.style = Binding(
            target=art_url.target,
            target_properties=art_url.target_properties,
            transform=lambda url: f"background-image: url('file://{url}');",
        )
        super().__init__(*args, **kwargs)


class TrackTitle(BaseWidget):
    base = widgets.Box
    css_classes = ["track-title"]
    hexpand = True
    vertical = True

    def __init__(self, title: Binding, *args, **kwargs):
        self.label_base = title
        super().__init__(*args, **kwargs)

    def render_child(self) -> widgets.Label:
        return widgets.Label(
            ellipsize="end",
            halign="start",
            label=self.label_base,
        )


class ArtistInfo(BaseWidget):
    base = widgets.Label
    __build_props__ = {"label", *BaseWidget.__build_props__}
    css_classes = ["artist"]
    halign = "start"
    ellipsize = "end"

    def __init__(self, artist: Binding, *args, **kwargs):
        self.label = artist
        super().__init__(*args, **kwargs)


class Controls(BaseWidget):
    base = widgets.CenterBox

    def __init__(self, service: MprisService, *args, **kwargs):
        self.service = service
        super().__init__(*args, **kwargs)

    def setup(self, widget: widgets.CenterBox) -> None:
        widget.center_widget = widgets.Box(
            child=[
                widgets.Button(
                    css_classes=["previous"],
                    on_click=lambda _: asyncio.create_task(self.service.previous()),
                    visible=self.service.can_go_previous,
                    cursor=cursor("pointer"),
                    child=widgets.Icon(image="media-skip-backward-symbolic"),
                ),
                widgets.Button(
                    css_classes=["play-pause"],
                    on_click=lambda _: asyncio.create_task(
                        self.service.play_pause_async()
                    ),
                    cursor=cursor("pointer"),
                    child=widgets.Icon(
                        image=self.service.bind(
                            "playback_status",
                            transform=lambda s: "media-playback-pause-symbolic"
                            if s == "Playing"
                            else "media-playback-start-symbolic",
                        ),
                    ),
                ),
                widgets.Button(
                    css_classes=["next"],
                    on_click=lambda _: asyncio.create_task(self.service.next_async()),
                    visible=self.service.can_go_next,
                    cursor=cursor("pointer"),
                    child=widgets.Icon(image="media-skip-forward-symbolic"),
                ),
            ]
        )
