import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set

from cfgtools.system import SystemPackage
from cfgtools.utils import cmd_output

IS_ARCH = shutil.which("pacman") is not None


def installed_pkgs() -> Set[str]:
    return {line.split(" ")[0] for line in cmd_output("pacman -Q")}


class Pacman(SystemPackage):
    def __init__(self, name: str):
        self.name = name
        if IS_ARCH:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    @classmethod
    def dry_run(cls, *pkgs: "Pacman") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(
                "# pacman -Syu --needed -y "
                f"{' '.join(list(to_be_installed))}"
            )

    @classmethod
    def apply(cls, *pkgs: "Pacman") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(f"Installing (pacman): {', '.join(list(to_be_installed))}")
            subprocess.run(
                ["sudo", "pacman", "-Syu", "--needed", "-y"]
                + list(to_be_installed)
            )


class AUR(SystemPackage):
    PRIORITY = 2
    LOOKUP_CACHE_FILE = (Path(__file__) / "../.aur_cache.json").resolve()
    lookup_cache: Dict[str, str] = {}

    def __init__(self, name: str, pkgs: Optional[Sequence[str]] = None):
        self.is_local = False
        self.pkgs = pkgs if pkgs else []

        if not IS_ARCH:
            return

        self._name = name
        if name.startswith("./"):
            self.local_path = name
            self.is_local = True

        super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        if not hasattr(self, "__name"):
            if self.LOOKUP_CACHE_FILE.exists():
                AUR.lookup_cache = json.loads(self.LOOKUP_CACHE_FILE.read_text())
            name = self._name
            if name.startswith("./"):
                if name in AUR.lookup_cache:
                    return AUR.lookup_cache[name]
                # if the name is defined as a relative path, we need to do some
                # parsing
                pkgbuild = Path(name)
                if not pkgbuild.exists():
                    raise FileNotFoundError(pkgbuild)
                if pkgbuild.is_dir():
                    if not (pkgbuild / "PKGBUILD").exists():
                        raise FileNotFoundError(pkgbuild / "PKGBUILD")
                    pkgbuild = pkgbuild / "PKGBUILD"

                self.__name = AUR.parse_name_pkgbuild(pkgbuild)
                AUR.lookup_cache[name] = self.__name
                self.LOOKUP_CACHE_FILE.write_text(json.dumps(AUR.lookup_cache))
            else:
                self.__name = name
        return self.__name

    @staticmethod
    def parse_name_pkgbuild(src: Path) -> str:
        srcinfo = (
            subprocess.run(
                ["makepkg", "--printsrcinfo", "-p", src.name],
                stdout=subprocess.PIPE,
                cwd=src.parent,
            )
            .stdout.decode("utf-8")
            .split("\n")
        )

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
    def filter(cls, pkgs: Sequence["AUR"]) -> List["AUR"]:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()

        if not to_be_installed:
            return []

        resolved_targets: List["AUR"] = []
        for pkg in pkgs:
            if pkg.name not in to_be_installed:
                continue

            resolved_targets.append(pkg)

        return resolved_targets

    @classmethod
    def convert_to_args(cls, pkgs: List["AUR"]) -> List[str]:
        deps: Set[str] = set()
        names: Set[str] = set()

        for pkg in pkgs:
            map(deps.add, pkg.pkgs)
            names.add(pkg.local_path if pkg.is_local else pkg.name)

        if deps:
            return ["--opts", ",".join(list(deps)), *list(names)]
        return list(names)

    @classmethod
    def dry_run(cls, *pkgs: "AUR") -> None:
        needed = cls.filter(pkgs)
        if needed:
            print(f"$ aur install {cls.convert_to_args(needed)}")

    @classmethod
    def apply(cls, *pkgs: "AUR") -> None:
        needed = cls.filter(pkgs)
        if needed:
            print(f"Installing (AUR): {', '.join(map(str, needed))}")
            if shutil.which("aur"):
                subprocess.run(
                    ["aur", "install"] + cls.convert_to_args(needed)
                )
            else:
                out = subprocess.run(
                    ["python", "./aur/aur.py", "install"]
                    + cls.convert_to_args(needed)
                )
                if out.returncode != 0:
                    print(
                        "AUR install failed, you have not set up the `aur` "
                        "helper (or installed it this run).  Make sure that "
                        "has been set up and run this again.  (This is a bit "
                        "of a chicken and egg problem)"
                    )
