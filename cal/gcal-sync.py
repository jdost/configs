#!/usr/bin/env python3

"""
TODO
- Add some helper args to allow a simple auth call to generate the token file
- Probably some logic to avoid running if there is no token file
"""

import datetime
import json
import os
import signal
from pathlib import Path
from typing import Dict, List, Optional, Set, Sequence

from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GcsaEvent

WINDOW = datetime.timedelta(days=90)
XDG_CONFIG_HOME = Path(
    os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
)
XDG_CACHE_HOME = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
XDG_DATA_HOME = Path(
    os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
)


class CalEvent:
    _id: str
    summary: str
    start: datetime.datetime
    end: datetime.datetime
    calendar: str

    def __init__(
            self,
            calendar: str = '',
            gcsa_src: Optional[GcsaEvent] = None,
            json_src: Optional[str] = None
    ):
        if gcsa_src is not None:
            self.calendar = calendar
            self._load_gcsa(gcsa_src)
        elif json_src is not None:
            self._load_json(json_src)
        else:
            raise ValueError(
                "Needs either a JSON based declaration or a GCSA Event"
            )

    def _load_gcsa(self, src) -> None:
        self._id = src.event_id
        self.summary = src.summary
        if not isinstance(src.start, datetime.datetime):
            src.start = datetime.datetime.combine(src.start, datetime.time.min)
        self.start = src.start
        if not isinstance(src.end, datetime.datetime):
            src.end = datetime.datetime.combine(src.end, datetime.time.min)
        self.end = src.end

    def _load_json(self, src) -> None:
        self._id = src["id"]
        self.summary = src["summary"]
        self.start = datetime.datetime.fromisoformat(src["start"])
        self.end = datetime.datetime.fromisoformat(src["end"])
        self.calendar = src["calendar"]

    @property
    def fingerprint(self) -> str:
        return hash(json.dumps(self.__json__()))

    @staticmethod
    def datetime_to_apt(src: datetime.datetime) -> str:
        return src.strftime("%m/%d/%Y @ %H:%M")

    def to_apt(self) -> str:
        return (
            f"{self.datetime_to_apt(self.start)} -> "
            f"{self.datetime_to_apt(self.end)}|{self.summary}"
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}({self._id}): {self.summary}"
            f"({self.start}-{self.end})>"
        )

    @classmethod
    def from_json(cls, src: Dict[str, str]) -> 'CalEvent':
        return cls(json_src=src)

    def __json__(self) -> Dict[str, str]:
        return {
            "id": str(self._id),
            "summary": self.summary,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "calendar": self.calendar,
        }


class LocalCache:
    FILE: Path = XDG_CACHE_HOME / "calcurse-gcal.json"

    def __init__(self):
        self._events: Dict[str, CalEvent] = {}
        now = datetime.datetime.now(datetime.timezone.utc)

        if self.FILE.exists():
            for raw_event in json.load(self.FILE.open()):
                event = CalEvent.from_json(raw_event)
                if event.end >= now:
                    self._events[event._id] = event

    @property
    def events(self) -> Set[str]:
        return set(self._events.keys())

    def __getitem__(self, key: str) -> CalEvent:
        return self._events[key]

    def __json__(self) -> Sequence[Dict[str, str]]:
        return [evt.__json__() for evt in self._events.values()]

    def update(self, new_events: Sequence[CalEvent]) -> None:
        json.dump(
            [evt.__json__() for evt in to_be_added.values()] + \
                self.__json__(),
            self.FILE.open("w")
        )


if __name__ == "__main__":
    calendar_file = XDG_CONFIG_HOME / "calcurse/calendars.txt"
    if not calendar_file.exists():
        calendar_file.touch()
        calendar_file.chmod(0o400)

    local_cache = LocalCache()
    to_be_added: Dict[str, CalEvent] = {}
    to_be_removed: List[CalEvent] = []
    now = datetime.datetime.now(datetime.timezone.utc)

    # ingest the remote events from the Google Calendars
    for calendar in calendar_file.read_text().strip().split("\n"):
        if not calendar:
            continue

        cal = GoogleCalendar(
            calendar,
            credentials_path=XDG_CONFIG_HOME / "calcurse/credentials.json",
            read_only=True,
        )

        for raw_event in cal.get_events(
            now,
            now + WINDOW,
            single_events=True,
            order_by="startTime"
        ):
            event = CalEvent(calendar, raw_event)
            to_be_added[event._id] = event

    # Collect anything that *was* on the remote previously but is no longer
    for key in local_cache.events - set(to_be_added.keys()):
        to_be_removed.append(local_cache[key])

    # Check all events that were previously added
    for key in local_cache.events & set(to_be_added.keys()):
        # check if the event was updated on the remote, if it is, remove the
        # old and re-add the updated event
        if local_cache[key].fingerprint != to_be_added[key].fingerprint:
            to_be_removed.append(local_cache[key])
        else:  # otherwise don't add an identical event
            del to_be_added[key]

    # If we have any changes to make, update the appointments file
    if len(to_be_removed) or len(to_be_added):
        # Start with the existing appointments
        calcurse_apts = set(
            (XDG_DATA_HOME / "calcurse/apts").read_text().strip().split("\n")
        )
        # Remove anything to be pruned and add anything to be added
        (XDG_DATA_HOME / "calcurse/apts").write_text(
            "\n".join(sorted(list(
                calcurse_apts
                    - set([e.to_apt() for e in to_be_removed])
                    | set([e.to_apt() for e in to_be_added])
            )))
        )
        # If there is a running calcurse, send an update
        if (XDG_DATA_HOME / "calcurse/.calcurse.pid").exists():
            print("updating")
            os.kill(
                int((XDG_DATA_HOME / "calcurse/.calcurse.pid").read_text()),
                signal.SIGUSR1,
            )

    local_cache.update(to_be_added.values())
