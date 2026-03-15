from ignis import widgets

from bar.icon import BarIcon
from utils.widgets import BaseWidget

from .bar_levels import LevelDotsIcon, StreamType


class SpeakerIcon(LevelDotsIcon):
    target = StreamType.speaker


class MicrophoneIcon(LevelDotsIcon):
    target = StreamType.microphone


class AudioIcon(BarIcon):
    name = "audio"
    priority = 11
    base = widgets.Box
    __build_props__ = BaseWidget.__build_props__
    css_classes = ["icon", "audio"]
    spacing = 0

    # TODO: this should be a BarIcon, but render using the BaseWidget
    def render_children(self) -> list[LevelDotsIcon]:
        return [
            SpeakerIcon(self.monitor_id).render(),
            MicrophoneIcon(self.monitor_id).render(),
        ]
