from datetime import datetime

from ignis.base_service import BaseService
from ignis.gobject import IgnisProperty
from ignis.services.mpris import MprisPlayer, MprisService
from ignis.utils import Poll

mpris = MprisService.get_default()
IGNORED_IF_STOPPED = {"qutebrowser"}


class PlayerMetadata:
    playing_since: datetime
    last_playing: datetime
    last_status: str
    ref: MprisPlayer
    name: str

    def __init__(self, ref: MprisPlayer) -> None:
        self.name = ref.identity
        self.ref = ref
        self.playing_since = datetime.min
        self.last_playing = datetime.min
        self.last_status = ""


class PlayerTracker(BaseService):
    _player_status: dict[str, PlayerMetadata]
    _current: MprisPlayer | None
    _UPDATE_FREQUENCY_MS: int = 10_000

    def __init__(self):
        super().__init__()

        for player in mpris.players:
            self._bind_player(player)
        mpris.connect("player-added", lambda _, player: self._bind_player(player))

        self._player_status = {}
        self._current = None
        self._current_status = "Stopped"

        self._update()
        self._poll = Poll(
            timeout=self._UPDATE_FREQUENCY_MS, callback=lambda _: self._update()
        )

    def _bind_player(self, player: MprisPlayer) -> None:
        player.connect("notify::playback-status", lambda _1, _2: self._update())
        self._update()

    def _update(self) -> None:
        current = datetime.now()
        previous_player = self._current
        unused_keys = set(self._player_status.keys())

        for player in mpris.players:
            if player.identity in unused_keys:
                unused_keys.remove(player.identity)

            metadata = self._player_status.get(player.identity, PlayerMetadata(player))
            if player.playback_status == "Playing":
                metadata.last_playing = current
            elif player.playback_status != metadata.last_status:
                if player.playback_status == "Playing":
                    metadata.playing_since = current
                metadata.last_status = player.playback_status
            self._player_status[player.identity] = metadata

        for unused_key in unused_keys:
            del self._player_status[unused_key]

        active: PlayerMetadata | None = None
        for metadata in self._player_status.values():
            # Ignore certain stopped players that just persist forever
            if (
                metadata.last_status == "Stopped"
                and metadata.name in IGNORED_IF_STOPPED
            ):
                continue

            if active is None:
                active = metadata
                continue

            if metadata.last_status == "Playing":
                if active.last_status != "Playing":
                    active = metadata
                    continue
                elif active.playing_since > metadata.playing_since:
                    active = metadata
                    continue
            elif active.last_status != "Playing":
                if metadata.last_playing > active.last_playing:
                    active = metadata
                    continue

        self._current = active.ref if active else None

        if previous_player is None and self._current is not None:
            self.notify("current_player")
        elif self._current is None:
            self.notify("current_player")
        elif previous_player is None:
            self.notify("current_player")
        elif previous_player.identity != self._current.identity:
            self.notify("current_player")

        if self._current is None:
            return
        elif self._current.playback_status != self._current_status:
            self._current_status = self._current.playback_status
            self.notify("status")

    @IgnisProperty
    def current_player(self) -> MprisPlayer | None:
        return self._current

    @IgnisProperty
    def status(self) -> str:
        return self._current_status
