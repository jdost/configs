from ignis import widgets
from sidebar.widget import SidebarWidget

from .services import PlayerTracker

player_tracker = PlayerTracker.get_default()

ICON_LOOKUP = {
    "Spotifyd": "spotify",
}
DEFAULT_ICON = "?"


class MprisSidebar(SidebarWidget):
    name = "mpris"

    def render_child(self) -> widgets.Box | None:
        current = player_tracker.current_player

        if current is None:
            return None

        return widgets.Box(
            hexpand=False,
            homogeneous=False,
            valign="start",
            child=[
                widgets.Icon(image=ICON_LOOKUP.get(current.identity, DEFAULT_ICON)),
                widgets.Label(label=current.bind("artist")),
                widgets.Label(label="-"),
                widgets.Label(label=current.bind("title"), ellipsize="end"),
            ],
        )
