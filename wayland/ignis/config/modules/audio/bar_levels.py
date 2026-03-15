from enum import Enum, auto

from ignis import widgets
from ignis.services.audio import AudioService, Stream

from bar.icon import BarIcon
from utils.widgets import BaseWidget

audio = AudioService.get_default()

BASE: str = "⡇"
DOTS: str = "⡀⠄⠂⠁"


class StreamType(Enum):
    speaker = auto()
    microphone = auto()


class LevelDotsIcon(BarIcon):
    target: StreamType

    base = widgets.Box
    __build_props__ = BaseWidget.__build_props__
    css_classes = ["leveldot-container"]

    @property
    def stream(self) -> Stream:
        if self.target is StreamType.speaker:
            return audio.speaker

        return audio.microphone

    def render_level(self, volume: float, muted: bool) -> str:
        resolved_volume = 0.0 if muted else (volume / 100.0)
        non_bool_index = int(resolved_volume * len(DOTS) // 1)
        for i, overlay in enumerate(self.overlay.overlays):
            if i < non_bool_index:
                opacity = 1.0
            elif i > non_bool_index:
                opacity = 0.0
            else:
                opacity = round(resolved_volume * len(DOTS) % 1, 3)

            overlay.style = f"opacity: {opacity:.1};"
        if muted:
            return "Volume: Muted"
        else:
            return f"Volume: {volume:.2%}"

    def setup_overlay(self, widget: widgets.Overlay) -> None:
        self.overlay = widget
        self.overlay.tooltip_text = self.stream.bind_many(
            ["volume", "is_muted"], transform=self.render_level
        )

    def render_child(self) -> widgets.Overlay:
        return widgets.Overlay(
            css_classes=["leveldot"],
            child=widgets.Label(label=BASE),
            overlays=[widgets.Label(label=d) for d in list(DOTS)],
            setup=lambda w: self.setup_overlay(w),
        )
