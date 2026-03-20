import ignis_ext.widgets as widgets_ext
from ignis import widgets
from ignis.services.audio import AudioService
from osd.hook import OSDHook

audio = AudioService.get_default()


class VolumeHook(OSDHook):
    name = "audio-volume"
    hook = (audio.speaker, ["notify::is-muted", "notify::volume"])

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.last_state = (audio.speaker.is_muted, audio.speaker.volume)

    def display(self, *args, **kwargs) -> None:
        if (
            audio.speaker.is_muted == self.last_state[0]
            and audio.speaker.volume == self.last_state[1]
        ):
            return

        super().display(*args, **kwargs)

    @staticmethod
    def resolve_icon(volume: float, muted: bool) -> str:
        if muted or volume < 1.0:
            return "audio-volume-muted"

        if volume > 67.0:
            return "audio-volume-high"
        elif volume > 34.0:
            return "audio-volume-medium"
        else:
            return "audio-volume-low"

    def render_children(self) -> list[widgets.Widget]:
        return [
            widgets.Icon(
                css_classes=["icon"],
                image=audio.speaker.bind_many(
                    ["volume", "is_muted"], self.resolve_icon
                ),
                pixel_size=29,
            ),
            widgets_ext.LevelBar(
                css_classes=audio.speaker.bind(
                    "is_muted", lambda m: ["muted"] if m else []
                ),
                max_value=1.5,
                mode="continuous",
                value=audio.speaker.bind("volume", transform=lambda v: v / 100),
                width_request=300,
            ),
        ]
