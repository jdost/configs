#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys

from pathlib import Path
from typing import Any, Dict, Sequence, Set

IMAGE_NAME="aur_builder"
PKG_FOLDER=os.environ.get("AURHOME", Path.home() / ".local/aur")
DROPBOX_REPO=Path.home() / ".local/dropbox/aur_repo"

if not PKG_FOLDER.is_dir():
    PKG_FOLDER.mkdir(parents=True)


class Package:
    AUR_QUERY_URL = "https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={}"

    def __init__(self, name: str, rebuild: bool = False):
        self.name = name
        self.is_local = Path(self.name).is_file()
        self.rebuild = rebuild
        self._aur_data = None
        self.is_git = self.name.endswith('-git')

    @classmethod
    def parse_arg(cls, arg: str) -> 'Package':
        if arg.endswith('!'):
            return cls(arg[:-1], rebuild=True)

        return cls(arg)

    @property
    def pkg_regex(self):
        return re.compile(f"^{self.name}-(.*)-(?:x86_64|any).pkg.tar.(?:xz|zst)$")

    @property
    def local_cache(self) -> Sequence[Path]:
        return sorted(PKG_FOLDER.glob(f"{self.name}*"))

    @property
    def shared_cache(self) -> Sequence[Path]:
        if not DROPBOX_REPO.exists() or not DROPBOX_REPO.is_dir():
            # There is no synced "repo" of built packages
            return []

        return sorted(DROPBOX_REPO.glob(f"{self.name}*"))

    @property
    def aur_data(self) -> Dict[str, Any]:
        if not self._aur_data:
            self._get_aur_data()

        return self._aur_data

    @property
    def latest_remote_version(self) -> str:
        if self.is_git:
            return "git"

        return self.aur_data["Version"]

    def _get_aur_data(self) -> None:
        import urllib.request

        self._aur_data = json.load(
            urllib.request.urlopen(self.AUR_QUERY_URL.format(self.name))
        )["results"][0]

    @property
    def needs_build(self) -> bool:
        if self.rebuild:
            return True

        available_cache = self.local_cache + self.shared_cache
        if self.is_git and available_cache:
            return False

        if not self.is_local:
            target = self.latest_remote_version
        else:
            srcinfo = subprocess.run(
                ["makepkg", "--printsrcinfo", "-p", self.name],
                stdout=subprocess.PIPE
            ).stdout.decode("utf-8").split()

            info = {}
            for line in srcinfo:
                try:
                    k, v = line.split("=", 1)
                    info[k.strip()] = v.strip()
                except ValueError:
                    continue

            target = "{pkgver}-{pkgrel}".format(**info)

        for cached_file in available_cache:
            match = self.pkg_regex.match(cached_file.name)
            if match and match.groups()[0] == target:
                return False

        return True

    @property
    def package_path(self) -> Path:
        available_cache = self.local_cache + self.shared_cache
        return sorted(available_cache)[0]


def build_image(rebuild: bool = False, force: bool = False) -> None:
    build_cmd = [
        "/usr/bin/docker",
        "build",
            "--force-rm",
            "--build-arg", f"UID={os.environ.get('UID', 1000)}",
            "--build-arg", f"GID={os.environ.get('GID', 1000)}",
            "-t", f"{IMAGE_NAME}:latest",
            "."
    ]

    images = subprocess.run(
        ["/usr/bin/docker", "images"],
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8").split("\n")

    if force:
        build_cmd.insert(2, "--no-cache")
    elif not rebuild:
        for image in images[1:]:
            try:
                name, tag, _ = image.split(None, 2)
            except ValueError:
                continue

            if name != IMAGE_NAME:
                continue
            if tag == "latest":
                return

    subprocess.run(
        build_cmd,
        cwd=Path(__file__).resolve().parent,
        check=True,
    )


if __name__ == "__main__":
    cmd = [
        "/usr/bin/docker",
        "run",
            "--rm",
            "-it",
            "-v", f"{PKG_FOLDER}:/pkgs"
    ]

    rebuild = False
    force = False

    pkgs = []
    action = "install"
    for target in sys.argv[1:]:
        if target == "--rebuild":
            rebuild = True
        elif target  == "--force":
            force = True
        elif target in {"build", "install", "sync"}:
            action = target
        else:
            pkgs.append(Package.parse_arg(target))

    if action == "sync":
        if not DROPBOX_REPO.exists():
            raise FileNotFoundError(DROPBOX_REPO)

        for pkg in pkgs:
            for local_pkg in (self.local_cache - self.shared_cache):
                print(f"Syncing {local_pkg.name} to shared cache...")
                (DROPBOX_REPO / local_pkg.name).write_bytes(local_pkg.read_bytes())

        sys.exit(0)

    to_be_built = [pkg.name for pkg in pkgs if pkg.needs_build]
    if to_be_built:
        build_image(rebuild, force)
        cmds = cmd + [f"{IMAGE_NAME}:latest"] + to_be_built
        print(f"$ {' '.join(cmds)}")
        subprocess.run(cmds, check=True)

    if action != "install":
        sys.exit(0)

    print(f"$ sudo pacman -U {' '.join(str(pkg.package_path) for pkg in pkgs)}")
    subprocess.run(["sudo", "pacman", "-U"] + [pkg.package_path for pkg in pkgs])
