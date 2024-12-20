import urllib.request
from pathlib import Path
from typing import Sequence, Tuple

import browsers.web_xdg_open
from cfgtools.files import DesktopEntry, UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import UserService, ensure_service
from cfgtools.utils import hide_xdg_entry

NAME = normalize(__name__)

packages = {Pacman("mpv"), Pacman("mpv-mpris"), Pacman("yt-dlp")}
files = {
    DesktopEntry(f"{NAME}/clipboard-video.desktop"),
    UserBin(f"{NAME}/clipboard-video.sh", "_clipboard-video"),
    UserService(f"{NAME}/clipboard-watcher.service"),
    XDGConfigFile(f"{NAME}/mpv.conf"),
    XDGConfigFile(f"{NAME}/yt-dlp", "yt-dlp/config"),
    browsers.web_xdg_open.SettingsFile(f"{NAME}/web-xdg-open", "mpv"),
}


@after
def grab_ytscripts() -> None:
    wanted_files: Sequence[Tuple[Path, str]] = [
        (XDGConfigFile.DIR / "mpv/yt-scripts/quality-menu.osc.lua",
         "https://github.com/christoph-heinrich/mpv-quality-menu/raw/refs/heads/master/quality-menu-osc.lua"),
        (XDGConfigFile.DIR / "mpv/yt-scripts/quality-menu.lua",
         "https://github.com/christoph-heinrich/mpv-quality-menu/raw/refs/heads/master/quality-menu.lua"),
        (XDGConfigFile.DIR / "mpv/script-opts/quality-menu.conf",
         "https://github.com/christoph-heinrich/mpv-quality-menu/raw/refs/heads/master/quality-menu.conf"),
    ]


    for loc, remote in wanted_files:
        if loc.exists():
            continue
        loc.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(remote) as req:
            loc.write_text(req.read().decode())


@after
def hide_unwanted_mpv_entries() -> None:
    [hide_xdg_entry(e) for e in ["qvidcap", "qv4l2"]]


@after
def enable_clipboard_watcher_service() -> None:
    ensure_service("clipboard-watcher.service", user=True)
