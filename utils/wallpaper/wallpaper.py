#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional, Sequence, Set
from urllib.parse import urlparse
from urllib.request import urlopen

CACHED_PROP_KEY = "__cached"
LOCK_FILE = Path(f"/run/user/{os.geteuid()}/wallpaper.lock")


def is_wayland() -> bool:
    """Detect whether being run in a wayland environment.

    NOTE: this is really just detecting hyprland, will need to re-adjust if ever
    used with a different WM."""
    if hasattr(is_wayland, CACHED_PROP_KEY):
        cached_prop = getattr(is_wayland, CACHED_PROP_KEY)
        assert isinstance(cached_prop, bool)
        return cached_prop

    hyprland_socket_locks = Path(f"/run/user/{os.geteuid()}/hypr/").glob("*/hyprland.lock")
    setattr(is_wayland, CACHED_PROP_KEY, bool(hyprland_socket_locks))
    return bool(hyprland_socket_locks)


def calc_humanreadable_size(total_bytes: int) -> str:
    """Convert a raw byte count into a human readable size w/ scaled prefixes

    ex.
    >>> calc_humanreadable_size(1024)
    "1 KB"
    >>> calc_humanreadable_size(102400)
    "100 KB"
    """
    PREFIXES = ["", "K", "M", "G", "T"]
    byte_size = float(total_bytes)
    for p in PREFIXES:
        if byte_size < 1024:
            return f"{byte_size:.2f}{p}B"
        byte_size = byte_size / 1024

    return ""


def is_locked() -> bool:
    """Checks whether wallpaper change locking is enabled."""
    return LOCK_FILE.exists()


def toggle_lock(state: Optional[bool] = None) -> bool:
    """Toggle the wallpaper change locking, explicit state if defined."""
    if state is None:
        state = not is_locked()

    if state:
        LOCK_FILE.touch()
    elif LOCK_FILE.exists():
        LOCK_FILE.unlink()

    return LOCK_FILE.exists()


class WallpaperSetter(ABC):
    @abstractmethod
    def get_monitors(self) -> Sequence[str]:
        pass

    @abstractmethod
    def set_wallpaper(self, wallpapers: Dict[str, Path]) -> None:
        pass


class HyprlandWallpaperSetter(WallpaperSetter):
    _signature: str
    _hyprctl: str
    def __init__(self):
        assert is_wayland(), \
            "This is meant to be used in a wayland environment."
        self._signature = self._get_signature()
        hyprctl = shutil.which("hyprctl")
        assert hyprctl is not None
        self._hyprctl = hyprctl

    def _get_signature(self) -> str:
        if "HYPRLAND_INSTANCE_SIGNATURE" in os.environ:
            instance = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
            if Path(f"/tmp/hypr/{instance}").exists():
                assert instance is not None
                return instance

        hyprland_socket_locks = list(
            Path(f"/run/user/{os.geteuid()}/hypr/").glob("*/hyprland.lock")
        )
        assert len(hyprland_socket_locks) == 1, \
            "There are too many hyprland locks."
        return hyprland_socket_locks[0].parent.stem

    def get_monitors(self) -> Sequence[str]:
        print(self._signature)
        monitors = json.loads(subprocess.run(
            [self._hyprctl, "monitors", "-j"],
            capture_output=True,
            env={"HYPRLAND_INSTANCE_SIGNATURE": self._signature},
        ).stdout)

        return {monitor["name"] for monitor in monitors}

    def set_wallpaper(self, wallpapers: Dict[str, Path]) -> None:
        print("unloading")
        subprocess.run([self._hyprctl, "hyprpaper", "unload", "all"], env={"HYPRLAND_INSTANCE_SIGNATURE": self._signature})

        for monitor, wallpaper in wallpapers.items():
            if wallpaper.is_symlink():
                wallpaper = wallpaper.resolve()

            print(f"Setting {monitor} wallpaper to {wallpaper}")
            subprocess.run([self._hyprctl, "hyprpaper", "preload", wallpaper], env={"HYPRLAND_INSTANCE_SIGNATURE": self._signature}, stdout=subprocess.DEVNULL)
            subprocess.run([self._hyprctl, "hyprpaper", "wallpaper", f"{monitor},{wallpaper}"], env={"HYPRLAND_INSTANCE_SIGNATURE": self._signature}, stdout=subprocess.DEVNULL)


class WallpaperSet:
    DEFAULT_WALLPAPER_LOC = Path.home() / ".local/dropbox/wallpaper"

    def __init__(self):
        pass

    @classmethod
    def folder(cls) -> Path:
        return Path(
            os.environ.get("WALLPAPER_FOLDER", cls.DEFAULT_WALLPAPER_LOC)
        )

    @property
    def _wallpapers(self) -> Sequence[Path]:
        cached_prop_key = f"{CACHED_PROP_KEY}:_wallpapers"
        if hasattr(self, cached_prop_key):
            cached_prop = getattr(self, cached_prop_key)
            assert isinstance(cached_prop, list)
            return cached_prop

        wallpaper_list = list(self.folder().iterdir())
        setattr(self, cached_prop_key, wallpaper_list)
        return wallpaper_list

    def count(self) -> int:
        return(len(self._wallpapers))

    def size(self) -> int:
        return sum([w.stat().st_size for w in self._wallpapers])

    def print_info(self) -> None:
        print(f"Count: {self.count()}")
        print(f" Size: {calc_humanreadable_size(self.size())}")

    def get_random(self) -> Path:
        return random.choice(self._wallpapers)


def update_wallpaper(setter: HyprlandWallpaperSetter, wallpapers: WallpaperSet) -> None:
    if is_locked():
        print("Wallpaper changing locked, unlock with `wallpaper unlock`")
        return
    wallpaper_updates: Dict[str, Path] = {}
    for monitor in setter.get_monitors():
        wallpaper = Path(f"/tmp/wallpaper.{monitor}")
        if wallpaper.exists():
            wallpaper.unlink()

        wallpaper.symlink_to(wallpapers.get_random())
        wallpaper_updates[monitor] = wallpaper

    setter.set_wallpaper(wallpaper_updates)


def upload_wallpapers(wallpapers: WallpaperSet) -> None:
    print("Paste in URLs, use `Ctrl-D` or empty input to stop...")
    uploads: Set[Path] = set()
    while True:
        try:
            target = input("Wallpaper URL: ")
            if target == "":
                break
        except EOFError:
            print("Done")
            break

        wallpaper = get_wallpaper(target)
        if wallpaper is None:
            print(f"Skipping, not a valid URL: {target}")
            continue
        print(f"Added as {wallpaper.name}")
        uploads.add(wallpaper)

    print(f"Total Retrieved: {len(uploads)}")
    print(f"     Total Size: {calc_humanreadable_size(sum([w.stat().st_size for w in uploads]))}")


def get_wallpaper(url: str) -> Optional[Path]:
    parsed = urlparse(url)
    if parsed.netloc == "":
        return None
    ext = Path(parsed.path).suffix
    with urlopen(url) as f:
        data = f.read()
        hash = hashlib.md5(data).hexdigest()
        filename = f"{str(hash)[:8]}{ext}"
        result = WallpaperSet.folder() / filename
        result.write_bytes(data)
        return result
    return None


parser = argparse.ArgumentParser(description="Wallpaper managing script.")
parser.add_argument(
    "command",
    nargs="?",
    choices=["set", "upload", "info", "lock", "unlock", "toggle"],
    default="set",
    help="Subcommand to run. (default: %(default)s)",
)


if __name__ == "__main__":
    args = parser.parse_args()
    setter = HyprlandWallpaperSetter()
    wallpapers = WallpaperSet()

    if args.command == "set":
        update_wallpaper(setter, wallpapers)
    elif args.command == "info":
        wallpapers.print_info()
    elif args.command == "upload":
        upload_wallpapers(wallpapers)
    elif args.command == "toggle":
        toggle_lock()
    elif args.command == "lock":
        toggle_lock(True)
    elif args.command == "unlock":
        toggle_lock(False)
