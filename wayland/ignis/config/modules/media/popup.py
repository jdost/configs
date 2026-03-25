from ignis import widgets
from popup.window import PopupWindow

from . import ui
from .services import PlayerTracker

player_tracker = PlayerTracker.get_default()


class MprisPopup(PopupWindow):
    name = "media"
    timeout = 5000

    def render_children(self) -> list[widgets.Widget]:
        return [
            ui.CoverArt(player_tracker.current_player.bind("art_url")).render(),
            widgets.Box(
                vertical=True,
                hexpand=True,
                child=[
                    ui.TrackTitle(player_tracker.current_player.bind("title")).render(),
                    ui.ArtistInfo(
                        player_tracker.current_player.bind("artist")
                    ).render(),
                    widgets.Box(vexpand=True),
                    ui.Controls(player_tracker.current_player).render(),
                ],
            ),
        ]
