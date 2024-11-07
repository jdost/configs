import os
import shlex
import subprocess
from getpass import getuser
from pathlib import Path
from typing import Sequence, Set

from cfgtools.files import BASE


def run(cmd: str) -> bool:
    resolved_cmd = shlex.split(cmd)

    return subprocess.run(
        resolved_cmd,
        stdout=subprocess.DEVNULL,
        cwd=BASE,
    ).returncode == 0


def cmd_output(cmd: str) -> Sequence[str]:
    resolved_cmd = shlex.split(cmd)

    return subprocess.run(
        resolved_cmd,
        stdout=subprocess.PIPE,
        cwd=BASE,
    ).stdout.decode("utf-8").split("\n")


def add_group(group: str) -> None:
    groups = subprocess.run(
        ["groups"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8").strip().split(" ")
    if group in groups:
        return

    print(f"Adding active user to the {group} group")
    subprocess.run(["sudo", "usermod", "-aG", group, getuser()])
    subprocess.run(["newgrp", group])


def hide_xdg_entry(entry: str) -> None:
    src_entry = Path(f"/usr/share/applications/{entry}.desktop")
    hidden_entry = Path.home() / f".local/share/applications/{entry}.desktop"

    if not src_entry.exists():
        print(f"Target entry ({src_entry}) doesn't exist, skipping...")
        return None

    if hidden_entry.exists():
        return None

    if not hidden_entry.parent.exists():
        hidden_entry.parent.mkdir(parents=True)

    print(f"Hiding XDG Desktop entry for: {entry}")
    hidden_entry.touch()
    hidden_entry.write_text(src_entry.read_text() + "\nNoDisplay=true")
    return None


def bins() -> Set[str]:
    bins = set()
    for p in os.environ["PATH"].split(":"):
        path_dir = Path(p)
        if path_dir.is_dir():
            bins |= {f.name for f in path_dir.iterdir()}

    return bins


def xdg_settings_get(key: str) -> str:
    cmd = subprocess.run(["xdg-settings", "get", key], stdout=subprocess.PIPE)
    assert cmd.returncode == 0, f"Command `xdg-settings get {key}` failed."
    return cmd.stdout.decode().strip()


def xdg_settings_set(key: str, val: str) -> None:
    subprocess.run(["xdg-settings", "set", key, val], check=True)
