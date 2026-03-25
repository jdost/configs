from bar.icon import BarIcon
from ignis import widgets
from ignis.services.mpris import MprisPlayer
from popup import popup

from utils import color

from .services import PlayerTracker

player_tracker = PlayerTracker.get_default()
ICON_LOOKUP: dict[str, tuple[str, color.Color]] = {
    "spotify": ("󰓇", color.Color(30, 215, 96)),
    "Spotifyd": ("󰓇", color.Color(30, 215, 96)),
    "firefox": ("󰈹", color.Color(230, 96, 0)),
    "chromium": ("", color.Color(0, 136, 247)),
    "qutebrowser": ("󰖟", color.Color(166, 223, 255)),
    "mpv": ("󰐌", color.Color(200, 100, 255)),
    "__default__": ("󰝚", color.Color(255, 255, 255)),
}


class MprisIcon(BarIcon):
    name = "media"
    priority = 5

    css_classes = ["media", "big"]

    def on_click(self, *_) -> None:
        if player_tracker.current_player is not None:
            popup.toggle(self.name)

    def render_icon(self, current: MprisPlayer | None, status: str) -> str:
        identity = current.identity if current else ""
        if identity and identity not in ICON_LOOKUP:
            print(f"Unset player key: {identity}")

        icon, color = ICON_LOOKUP.get(identity, ICON_LOOKUP["__default__"])
        self.icon_widget.style = (
            f"color: {color.as_rgb()};"
            if status == "Playing"
            else "color: rgb(153, 153, 153);"
        )
        self.icon_widget.tooltip_text = (
            (f"{current.identity}: {current.playback_status}") if current else ""
        )

        return icon

    def setup(self, icon: widgets.Button) -> None:
        self.icon_widget = widgets.Label()
        self.icon_widget.label = player_tracker.bind_many(
            ["current_player", "status"], transform=self.render_icon
        )
        icon.child = self.icon_widget
        self.render_icon(player_tracker.current_player, player_tracker.status)
