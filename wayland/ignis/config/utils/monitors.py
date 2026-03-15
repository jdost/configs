from typing import Sequence

from ignis.services.hyprland import HyprlandMonitor, HyprlandService

hyprland = HyprlandService.get_default()

_monitors: Sequence[HyprlandMonitor] = []


def get_monitors() -> Sequence[int]:
    global _monitors

    if not _monitors:
        _monitors = hyprland.get_monitors()

    return [m.id for m in _monitors]


def primary() -> int:
    # TODO see if there's some idea of a primary, otherwise remove this or
    # manage via per-machine settings
    return 0


def focused() -> int:
    global _monitors

    if not _monitors:
        _monitors = hyprland.get_monitors()

    for m in _monitors:
        if m.focused:
            return m.id

    return 0  # ??? a monitor *should* be focused
