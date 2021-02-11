#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys

from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Set

IMAGE_NAME="aur_builder"
PKG_FOLDER=os.environ.get("AURHOME", Path.home() / ".local/aur")
DROPBOX_REPO=Path.home() / ".local/dropbox/aur"

if not PKG_FOLDER.is_dir():
    PKG_FOLDER.mkdir(parents=True)


def get_version_from_path(prefix: str, src: Path) -> str:
    match = re.compile(f"{prefix}-(.+)-(?:x86_64|any).pkg.tar.(?:xz|zst)$").match(src.name)
    if not match:
        return ""

    return match.groups()[0]


def parse_version(version_str: str) -> Sequence[int]:
    version, patch = version_str.split("-", 1)
    return [int(n) for n in version.split(".") + [patch]]


class Package:
    AUR_QUERY_URL = "https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={}"

    def __init__(self, name: str, rebuild: bool = False, latest: bool = False):
        self.latest = latest
        self.is_local = Path(name).is_file()
        self.name = Path(name).resolve().name if self.is_local else name
        self.path = Path(name).resolve() if self.is_local else None
        self.rebuild = rebuild
        self._aur_data = None
        self.is_git = self.name.endswith('-git')

    @classmethod
    def parse_arg(cls, arg: str) -> 'Package':
        """ parse the package argument name into the package flags:
        normal: `foo`
        use latest package: `foo!`
        build regardless of cache: `foo!!`
        """
        kwargs={}
        name=arg

        if name.endswith('!'):
            name = name[:-1]
            kwargs['latest'] = True
        if name.endswith('!'):
            name = name[:-1]
            kwargs['rebuild'] = True

        return cls(name, **kwargs)

    @property
    def docker_volume_mount(self) -> str:
        return f"{self.path}:/src/{self.path.name}"

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
            return self.latest

        if not self.latest:
            return not available_cache

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
            if get_version_from_path(self.name, cached_file) == target:
                return False

        return True

    @property
    def package_path(self) -> Path:
        available_cache = self.local_cache + self.shared_cache
        parser = lambda x: x if self.is_git else parse_version
        return [p for p in sorted(
            available_cache,
            key=lambda p: parser(get_version_from_path(self.name, p)),
        )][-1]

    @property
    def available_versions(self) -> Sequence[str]:
        available_cache = self.local_cache + self.shared_cache
        return [get_version_from_path(self.name, p) for p in sorted(
            available_cache,
            key=lambda p: parse_version(get_version_from_path(self.name, p)),
        )]


def build_image(
    rebuild: bool = False, force: bool = False, as_root: bool = False
) -> None:
    """The `as_root` is a kind of bootstrapping hack that allows this to run
    if the user is not yet with the docker group.
    """
    docker_cmd = ["sudo", "/usr/bin/docker"] if as_root else ["/usr/bin/docker"]
    build_cmd = docker_cmd + [
        "build",
            "--force-rm",
            "--build-arg", f"UID={os.environ.get('UID', 1000)}",
            "--build-arg", f"GID={os.environ.get('GID', 1000)}",
            "-t", f"{IMAGE_NAME}:latest",
            "."
    ]

    images = subprocess.run(
        docker_cmd + ["images"],
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


def print_help() -> None:
    print(f"{sys.argv[0]} [--rebuild] [--force] <COMMAND> [packages...]")
    print("""
Docker based AUR package builder script.  This attempts to manage building AUR
packages and caching them locally and in my dropbox folder.

Commands:
\tinstall\tInstall the "best" version of each package from the AUR
\tbuild\tBuild (but don't install) the "best" version of each package from the AUR
\tsync\tSynchronize locally built AUR packages to the shared dropbox cache
\tlist\tList versions for the packages available that are already built

Flags:
\t--rebuild\tBuild a new docker building image if needed
\t--force\tBuild a new docker building image regardless of state

Package Syntax:
  By default, will just install the most recent package in the available cache,
  with a single '!' suffix, will determine if the available cache has the most
  recent version from the AUR built.  With a '!!' suffix, will rebuild
  regardless of what is in the cache.
""")


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
        elif target in {"build", "install", "sync", "list"}:
            action = target
        elif target in {"help", "--help", "-h"}:
            print_help()
            sys.exit(0)
        else:
            pkg = Package.parse_arg(target)
            pkgs.append(pkg)
            if pkg.is_local:
                cmd += ["-v", pkg.docker_volume_mount]

    if action == "list":
        for pkg in pkgs:
            print(f"{pkg.name} Versions:")
            print("    " + '\t'.join(pkg.available_versions))

        sys.exit(0)

    if action == "sync":
        if not DROPBOX_REPO.exists():
            raise FileNotFoundError(DROPBOX_REPO)

        for pkg in pkgs:
            unsynced_pkgs = (
                set(p.name for p in pkg.local_cache) - \
                set(p.name for p in pkg.shared_cache)
            )
            for local_pkg in [p for p in pkg.local_cache if p.name in unsynced_pkgs]:
                print(f"Syncing {local_pkg.name} to shared cache...")
                (DROPBOX_REPO / local_pkg.name).write_bytes(local_pkg.read_bytes())

        sys.exit(0)

    to_be_built = [pkg.name for pkg in pkgs if pkg.needs_build]
    if to_be_built:
        # checks if docker is running and attempts to start it if it isn't
        if subprocess.run(
            ["systemctl", "status", "docker"], stdout=subprocess.PIPE
        ).returncode != 0:
            if subprocess.run(
                ["sudo", "systemctl", "start", "docker"]
            ).returncode != 0:
                print(
                    "ERROR: You are attempting to run a docker command without a "
                    "running docker daemon.  Please ensure that is running..."
                )
                sys.exit(1)

        # checks if the user can talk to docker (due to the guid limitation),
        #   if not, then runs all the docker commands are root
        my_groups = subprocess.run(
            ["groups"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8").split(" ")
        if "docker" not in my_groups:
            cmd = ["sudo"] + cmd
            build_image(rebuild, force, as_root=True)
        else:
            build_image(rebuild, force)

        cmds = cmd + [f"{IMAGE_NAME}:latest"] + to_be_built
        print(f"$ {' '.join(cmds)}")
        subprocess.run(cmds, check=True)

    if action != "install":
        sys.exit(0)

    print(f"$ sudo pacman -U {' '.join(str(pkg.package_path) for pkg in pkgs)}")
    subprocess.run(["sudo", "pacman", "-U"] + [pkg.package_path for pkg in pkgs])
