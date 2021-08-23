#!/usr/bin/env python3

"""
TODO
- Add some helper args to allow a simple auth call to generate the token file
"""

import datetime
import json
import os
import signal
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Sequence

from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as GcsaEvent
from google.auth.exceptions import RefreshError

import pytz

DEFAULT_TZ = pytz.timezone("US/Pacific")
WINDOW = datetime.timedelta(days=90)
XDG_CONFIG_HOME = Path(
    os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
)
XDG_CACHE_HOME = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
XDG_DATA_HOME = Path(
    os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
)
SYSTEMD_RUN = "MANAGERPID" in os.environ


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
            src.start = datetime.datetime.combine(
                src.start, datetime.time.min, tzinfo=DEFAULT_TZ
            )
        self.start = src.start
        if not isinstance(src.end, datetime.datetime):
            src.end = datetime.datetime.combine(
                src.end, datetime.time.min, tzinfo=DEFAULT_TZ
            )
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

    def __str__(self) -> str:
        return f"{self.summary} ({self.start})"

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
        now = datetime.datetime.now(tz=DEFAULT_TZ)

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

    def remove(self, key: str) -> None:
        del self._events[key]

    def update(self, new_events: Sequence[CalEvent]) -> None:
        json.dump(
            [evt.__json__() for evt in to_be_added.values()] + \
                self.__json__(),
            self.FILE.open("w")
        )


if __name__ == "__main__":
    # If this is triggered by the systemd timer before the user has done the
    # auth flow to get the token, error out quickly and provide a log line
    if (
        SYSTEMD_RUN and
        not (XDG_CONFIG_HOME / "calcurse/token.pickle").exists()
    ):
        print("Please run this from your terminal to perform the initial auth")
        sys.exit(1)
    elif SYSTEMD_RUN:
        import webbrowser

        def fake_register_standard_browsers():
            import subprocess

            res = subprocess.run([
                "notify-send",
                "--icon",
                "calendar",
                "--app-name",
                "gcal-sync",
                "--expire-time",
                str(1000 * 30),
                "GCal Sync Failed",
                "Token probably expired, run manually to refresh"
            ], check=True)
            raise ImportError("webbrowser doesn't work in a headless setting.")
        webbrowser.register_standard_browsers = fake_register_standard_browsers

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

        try:
            cal = GoogleCalendar(
                calendar,
                credentials_path=XDG_CONFIG_HOME / "calcurse/credentials.json",
                read_only=True,
            )
        except RefreshError:
            token = XDG_CONFIG_HOME / "calcurse/token.pickle"
            if token.exists():
                token.unlink()
            print("Token expired.  Re-auth manually...")
            sys.exit(1)

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
        local_cache.remove(key)

    # Check all events that were previously added
    for key in local_cache.events & set(to_be_added.keys()):
        # check if the event was updated on the remote, if it is, remove the
        # old and re-add the updated event
        if local_cache[key].fingerprint != to_be_added[key].fingerprint:
            to_be_removed.append(local_cache[key])
            local_cache.remove(key)
        else:  # otherwise don't add an identical event
            del to_be_added[key]

    # If we have any changes to make, update the appointments file
    if len(to_be_removed) or len(to_be_added):
        if len(to_be_added):
            print(f"Adding {len(to_be_added)}...")
            for apt in to_be_added.values():
                print(apt)
        if len(to_be_removed):
            print(f"Removing {len(to_be_removed)}...")
            for apt in to_be_removed:
                print(apt)
        # Start with the existing appointments
        calcurse_apts = set(
            (XDG_DATA_HOME / "calcurse/apts").read_text().strip().split("\n")
        )
        # Remove anything to be pruned and add anything to be added
        (XDG_DATA_HOME / "calcurse/apts").write_text(
            "\n".join(sorted(list(
                calcurse_apts
                    - set([e.to_apt() for e in to_be_removed])
                    | set([e.to_apt() for e in to_be_added.values()])
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
