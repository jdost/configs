import os
import shlex
import subprocess

from getpass import getuser
from pathlib import Path
from typing import Sequence
from cfgtools.files import BASE


def cmd_output(cmd: str) -> Sequence[str]:
    resolved_cmd = shlex.split(cmd)

    return subprocess.run(
        resolved_cmd,
        stdout=subprocess.PIPE,
        cwd=BASE,
    ).stdout.decode("utf-8").split()


def add_group(group: str) -> None:
    groups = os.getgroups()
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
