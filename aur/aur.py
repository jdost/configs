#!/usr/bin/env python3

import os
import subprocess
import sys

from pathlib import Path

IMAGE_NAME="aur_builder"
PKG_FOLDER=os.environ.get("AURHOME", Path.home() / ".local/aur")
if not PKG_FOLDER.is_dir():
    PKG_FOLDER.mkdir(parents=True)


def build_image(rebuild: bool = False, force: bool = False) -> None:
    build_cmd = [
        "docker",
        "build",
            "--force-rm",
            "--build-arg", f"UID={os.environ.get('UID', 1000)}",
            "--build-arg", f"GID={os.environ.get('GID', 1000)}",
            "-t", f"{IMAGE_NAME}:latest",
            "."
    ]

    images = subprocess.run(
        ["docker", "images"],
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
        "docker",
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
        elif target in {"build", "install"}:
            action = target
        elif Path(target).exists():
            t = Path(target).resolve()
            cmd += ["-v", f"{t}:/src/{t.name}"]
            pkgs.append(t.name)
        else:
            pkgs.append(target)

    build_image(rebuild, force)
    subprocess.run(
        cmd + [f"{IMAGE_NAME}:latest"] + pkgs,
        check=True,
    )
    if action != "install":
        sys.exit(0)

    for pkg in pkgs:
        available = sorted(PKG_FOLDER.glob(f"{pkg}*"))
        if available:
            subprocess.run(["sudo", "pacman", "-U", available[0]])
