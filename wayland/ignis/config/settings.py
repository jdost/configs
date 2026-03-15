import json
from pathlib import Path

accent: bool = True
font_size: int = 18
modules: list[str] = ["audio", "clock", "cpu", "hyprland", "memory", "systray"]
sidebar: bool = True

__SETTINGS = Path.home() / ".config/ignis/settings.json"

if __SETTINGS.exists():
    for key, value in json.loads(__SETTINGS.read_text()).items():
        globals()[key] = value
