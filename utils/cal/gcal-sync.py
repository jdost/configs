#!/usr/bin/env python3

import hashlib
import json
import os
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

import icalendar

XDG_CONFIG_HOME = Path(
    os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
)
XDG_CACHE_HOME = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
XDG_DATA_HOME = Path(
    os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
)
MIN_DATE = datetime.now(UTC) - timedelta(days=365)
LOCALTZ = ZoneInfo.from_file(Path("/etc/localtime").open("rb"))  # get local tz from system


@dataclass
class Event:
    start: datetime
    end: datetime
    uid: str
    summary: str
    description: Optional[str]

    @classmethod
    def from_ical(cls, event: icalendar.Event) -> "Event":
        return cls(
            start=(
                event.start if isinstance(event.start, datetime)
                else datetime(event.start.year, event.start.month, event.start.day)
            ).astimezone(UTC),
            end=(
                event.end if isinstance(event.end, datetime)
                else datetime(event.end.year, event.end.month, event.end.day)
            ).astimezone(UTC),
            uid=event.get('UID'),
            summary=event.get('SUMMARY'),
            description=event.get('DESCRIPTION'),
        )

    @classmethod
    def from_json(cls, serialization: Dict[str, Any]) -> "Event":
        for k in ["start", "end", "uid", "summary"]:
            assert k in serialization and isinstance(serialization[k], str), f"{k} missing"

        return cls(
            start=datetime.fromisoformat(serialization["start"]).astimezone(UTC),
            end=datetime.fromisoformat(serialization["end"]).astimezone(UTC),
            uid=serialization["uid"],
            summary=serialization["summary"],
            description=serialization.get("description"),
        )

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256((
            f"{self.uid}{self.start.isoformat()}{self.end.isoformat()}{self.summary}"
        ).encode()).hexdigest()

    def __repr__(self) -> str:
        return (
            f"<Event: {self.start.strftime('%Y-%M-%d %H:%M')} "
            f"- {self.summary}>"
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "uid": self.uid,
            "summary": self.summary,
            "description": self.description,
        }


class RemoteCalendar:
    def __init__(self, url: str):
        self.remote_url = url
        self._events: Dict[str, Event] = {}
        self._loaded = False

    @contextmanager
    def calendar(self):
        with urllib.request.urlopen(self.remote_url) as ics_file:
            yield icalendar.Calendar.from_ical(ics_file.read())

    def load(self) -> None:
        with self.calendar() as cal:
            for ics_event in cal.walk('VEVENT'):
                # Just filter out anything older than a year
                if isinstance(ics_event.start, datetime):
                    if ics_event.start < MIN_DATE:
                        continue
                elif ics_event.start < MIN_DATE.date():
                    continue
                event = Event.from_ical(ics_event)
                self._events[event.uid] = event

        self._loaded = True

    @property
    def events(self) -> Dict[str, Event]:
        if not self._loaded:
            self.load()
        return self._events


class LocalCache:
    FILE: Path = XDG_CACHE_HOME / "calcurse-gcal.json"

    def __init__(self, remote_url: str):
        self.events: Dict[str, Event] = {}
        self._key = remote_url

        if self.FILE.exists():
            calendars = json.load(self.FILE.open())
            for serialized_event in calendars.get(self._key, []):
                event = Event.from_json(serialized_event)
                if event.start >= MIN_DATE:
                    self.events[event.uid] = event
        else:
            self.FILE.write_text("{}")

    def update(self, replacement: Dict[str, Event]) -> None:
        base = json.load(self.FILE.open())
        base[self._key] = [event.to_json() for event in replacement.values()]
        json.dump(base, self.FILE.open("w"))


class CalCurseCalendar:
    DIR: Path = XDG_DATA_HOME / "calcurse"
    STRFTIME = "%m/%d/%Y @ %H:%M"

    def __init__(self):
        self.load()

    def load(self) -> None:
        self.dirty = False
        apts_file = self.DIR / "apts"
        if apts_file.exists():
            self.apts = set(
                (self.DIR / "apts").read_text().strip().split("\n")
            )
        else:
            apts_file.parent.mkdir(parents=True, exist_ok=True)
            apts_file.touch()
            self.apts = set()

    def save(self) -> None:
        # Skip saving if nothing has changed
        if not self.dirty:
            return

        self.dirty = False
        (self.DIR / "apts").write_text("\n".join(sorted(list(self.apts))))

    def add(self, event: Event) -> None:
        apt = (
            f"{event.start.astimezone(LOCALTZ).strftime(self.STRFTIME)} -> "
            f"{event.end.astimezone(LOCALTZ).strftime(self.STRFTIME)}"
        )
        if event.description:
            note_fingerprint = hashlib.sha1(event.description.encode()).hexdigest()
            (self.DIR / f"notes/{note_fingerprint}").write_text(event.description)
            apt += f">{note_fingerprint} "
        apt += f"|{event.summary}"

        self.dirty = True
        self.apts.add(apt)

    def remove(self, event: Event) -> None:
        apt = (
            f"{event.start.astimezone(LOCALTZ).strftime(self.STRFTIME)} -> "
            f"{event.end.astimezone(LOCALTZ).strftime(self.STRFTIME)}"
        )
        if event.description:
            note_fingerprint = hashlib.sha1(event.description.encode()).hexdigest()
            note_file = self.DIR / f"notes/{note_fingerprint}"
            if note_file.exists():
                note_file.unlink()
            apt += f">{note_fingerprint} "
        apt += f"|{event.summary}"

        self.dirty = True
        self.apts.remove(apt)


if __name__ == "__main__":
    calendar_file = XDG_CONFIG_HOME / "calcurse/calendars.txt"
    if not calendar_file.exists():
        calendar_file.touch()
        calendar_file.chmod(0o400)

    calcurse = CalCurseCalendar()
    for url in calendar_file.read_text().strip().split("\n"):
        if not url:
            continue

        # Load remote and local, get uid sets from each and compare with:
        remote = RemoteCalendar(url)
        local = LocalCache(url)

        # - overlap, check each to see if the fingerprint changed, update
        #   any fingerprint mismatches as they have changed
        for key in remote.events.keys() & local.events.keys():
            if remote.events[key] != local.events[key]:
                # find local.event in calendar, remove and add remote.event
                print(f"Event updated: {local.events[key]} -> {remote.events[key]}")
                calcurse.remove(local.events[key])
                calcurse.add(remote.events[key])

        # - missing from the local, add the events
        for key in remote.events.keys() - local.events.keys():
            print(f"New Event: {remote.events[key]}")
            calcurse.add(remote.events[key])

        # - missing from remote, delete the events
        for key in local.events.keys() - remote.events.keys():
            print(f"Old Event: {local.events[key]}")
            calcurse.remove(local.events[key])

        local.update(remote.events)

    calcurse.save()
