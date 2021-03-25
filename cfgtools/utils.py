import shlex
import subprocess

from getpass import getuser
from pathlib import Path
from typing import Sequence
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

    subprocess.run(["sudo", "usermod", "-aG", group, getuser()])
    subprocess.run(["newgrp", group])


def hide_xdg_entry(entry: str) -> None:
    src_entry = Path(f"/usr/share/applications/{entry}.desktop")
    hidden_entry = Path.home() / f".local/share/applications/{entry}.desktop"

    if hidden_entry.exists():
        return

    if not hidden_entry.parent.exists():
        hidden_entry.parent.mkdir(parents=True)

    hidden_entry.touch()
    hidden_entry.write_text(src_entry.read_text() + "\nNoDisplay=true")
