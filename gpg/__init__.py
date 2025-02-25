import urllib.request
from pathlib import Path

from cfgtools import utils
from cfgtools.files import (HOME, EnvironmentFile, File, Folder, XinitRC,
                            normalize)
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service
from wayland import WaylandRC

NAME = normalize(__name__)
USER_GPG_FOLDER = HOME / ".local/gpg"
GPG_CONFIG_FILES = ["gpg.conf", "gpg-agent.conf", "scdaemon.conf"]
# This is a sharable public link via dropbox
KEYID = "061ABE27128D52FCBAF4A3F7570D47FF2073CDA5"
PUBKEY_URL = "https://www.dropbox.com/scl/fi/prcdjw7cj775rmsf1tftx/pubkey.gpg?rlkey=r939kpxou6pszn4tmvti42elx&st=wyivlveq&dl=0"

packages={Pacman("gnupg"), Pacman("pcsclite"), Pacman("ccid"), Pacman("gcr")}
files=[
    EnvironmentFile(NAME),
    Folder(USER_GPG_FOLDER, permissions=0o700),
    XinitRC(NAME, priority=20),
    WaylandRC(f"{NAME}/waylandrc", "gpg", priority=20),
] + [File(f"{NAME}/{f}", USER_GPG_FOLDER / f) for f in GPG_CONFIG_FILES]


@after
def smartcard_daemon_running() -> None:
    ensure_service("pcscd.socket")


@after
def import_pubkey() -> None:
    if utils.run(f"gpg --list-keys {KEYID}"):
        return

    tmp_key = Path(USER_GPG_FOLDER) / "pubkey"
    with urllib.request.urlopen(PUBKEY_URL) as req:
        tmp_key.write_bytes(req.read())

    utils.run(f"gpg --import {tmp_key}")
    # Tried to auto do this, gpg doesn't want programmatic interfacing
    print(f"Please run `gpg --edit-key {KEYID}` and mark the key as trusted.")
