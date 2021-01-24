import shutil
import subprocess

from pathlib import Path
from typing import Set, Sequence

from cfgtools.system import SystemPackage
from cfgtools.utils import cmd_output

IS_ARCH = shutil.which('pacman') != None


def installed_pkgs() -> Set[str]:
    return {
        l.split(" ")[0] for l in cmd_output("pacman -Q")
    }


class Pacman(SystemPackage):
    def __init__(self, name: str):
        self.name = name
        if IS_ARCH:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    @classmethod
    def dry_run(cls, *pkgs: 'Pacman') -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(f"# pacman -Syu --needed -y {' '.join(to_be_installed)}")

    @classmethod
    def apply(cls, *pkgs: 'Pacman') -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(f"Installing (pacman): {', '.join(list(to_be_installed))}")
            subprocess.run(
                ["sudo", "pacman", "-Syu", "--needed", "-y"] +
                list(to_be_installed)
            )


class AUR(SystemPackage):
    def __init__(self, name: str):
        self.is_local = False

        if name.startswith("./"):
            # if the name is defined as a relative path, we need to do some
            # parsing
            pkgbuild = Path(name)
            if not pkgbuild.exists():
                raise FileNotFoundError(pkgbuild)
            if pkgbuild.is_dir():
                if not (pkgbuild / "PKGBUILD").exists():
                    raise FileNotFoundError(pkgbuild / "PKGBUILD")
                pkgbuild = pkgbuild / "PKGBUILD"

            self.name = AUR.parse_name_pkgbuild(pkgbuild)
            self.local_path = name
            self.is_local = True
        else:
            self.name = name

        if IS_ARCH:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    @staticmethod
    def parse_name_pkgbuild(src: Path) -> str:
        srcinfo = subprocess.run(
            ["makepkg", "--printsrcinfo", "-p", src.name],
            stdout=subprocess.PIPE,
            cwd=src.parent,
        ).stdout.decode("utf-8").split("\n")

        for line in srcinfo:
            try:
                k, v = line.split("=", 1)
                if k.strip() == "pkgname":
                    return v.strip()
            except ValueError:
                continue

        # this should not be reached
        raise ValueError()

    @classmethod
    def filter(cls, pkgs: Sequence['AUR']) -> Sequence['AUR']:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()

        if not to_be_installed:
            return []

        resolved_targets = []
        for pkg in pkgs:
            if pkg.name not in to_be_installed:
                continue

            resolved_targets.append(
                pkg.local_path if pkg.is_local else pkg.name
            )

        return resolved_targets

    @classmethod
    def dry_run(cls, *pkgs: 'AUR') -> None:
        needed = cls.filter(pkgs)
        if needed:
            print(f"$ aur install {' '.join(needed)}")

    @classmethod
    def apply(cls, *pkgs: 'AUR') -> None:
        needed = cls.filter(pkgs)
        if needed:
            print(f"Installing (AUR): {', '.join(needed)}")
            if shutil.which("aur"):
                subprocess.run(["aur", "install"] + needed)
            else:
                out = subprocess.run(
                    ["python", "./aur/aur.py", "install"] + needed
                )
                if out.returncode != 0:
                    print(
                        "AUR install failed, you have not set up the `aur` "
                        "helper (or installed it this run).  Make sure that "
                        "has been set up and run this again.  (This is a bit "
                        "of a chicken and egg problem)"
                    )
