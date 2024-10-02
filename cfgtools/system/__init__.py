import getpass
import os
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Optional, Sequence

from cfgtools.files import InputType

_SUDO_CHSH = False
registered_packages = defaultdict(set)


class SystemPackage:
    PRIORITY = 1

    def __init__(self):
        registered_packages[self.__class__].add(self)

    def __repr__(self) -> str:
        return str(self.__class__)


def setup(dry_run: bool = False) -> None:
    global registered_packages

    for pkg_class in sorted(registered_packages, key=lambda p: p.PRIORITY):
        pkgs = registered_packages[pkg_class]
        if dry_run:
            pkg_class.dry_run(*pkgs)
        else:
            pkg_class.apply(*pkgs)


class GitRepository(SystemPackage):
    PRIORITY = 10
    BASE_DIR = Path.home() / "src"

    def __init__(self, remote: InputType, name: Optional[InputType] = None):
        self.remote = str(remote)
        if not name:
            _, name = self.remote.rsplit("/", 1)
            if name.endswith(".git"):
                name = name[:-4]

            self.name = self.BASE_DIR / name
        elif isinstance(name, Path):
            self.name = name
        else:
            self.name = self.BASE_DIR / name
        super().__init__()

    @property
    def local_path(self) -> Path:
        return self.name

    @classmethod
    def dry_run(cls, *repos: "GitRepository") -> None:
        for repo in repos:
            repo._dry_run()

    def _dry_run(self) -> None:
        if self.local_path.exists():
            return

        print(f"$ git clone {self.remote} {self.local_path}")

    @classmethod
    def apply(cls, *repos: "GitRepository") -> None:
        for repo in repos:
            repo._apply()

    def _apply(self) -> None:
        if self.local_path.exists():
            return

        subprocess.run(["git", "clone", self.remote, self.local_path])

    def run_in(self, cmd: Sequence[str]) -> None:
        subprocess.run(cmd, cwd=self.local_path)


def set_default_shell(shell_bin: str) -> None:
    from cfgtools.hooks import after

    @after
    def change_user_shell() -> None:
        if os.environ.get("SHELL") == shell_bin:
            return

        if _SUDO_CHSH:
            subprocess.run(
                ["sudo", "chsh", "-s", shell_bin, getpass.getuser()]
            )
        else:
            subprocess.run(["chsh", "-s", shell_bin])
