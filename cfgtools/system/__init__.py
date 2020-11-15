import subprocess

from collections import defaultdict
from pathlib import Path
from typing import Optional, Sequence

registered_packages = defaultdict(set)


class SystemPackage:
    def __init__(self):
        registered_packages[self.__class__].add(self)

    def __repr__(self) -> str:
        return str(self.__class__)


def setup(dry_run: bool = False) -> None:
    global registered_packages

    for pkg_class, pkgs in registered_packages.items():
        if dry_run:
            pkg_class.dry_run(*pkgs)
        else:
            pkg_class.apply(*pkgs)


class GitRepository(SystemPackage):
    BASE_DIR = Path.home() / "src"

    def __init__(self, remote: str, name: Optional[str] = None):
        self.remote = remote
        if not name:
            _, name = remote.rsplit("/", 1)
            if name.endswith(".git"):
                name = name[:-4]

        self.name = name
        super().__init__()

    @property
    def local_path(self) -> Path:
        return GitRepository.BASE_DIR / self.name

    @classmethod
    def dry_run(cls, *repos: 'GitRepository') -> None:
        for repo in repos:
            repo.dry_run()

    def dry_run(self) -> None:
        if self.local_path.exists():
            return

        print(f"$ git clone {self.remote} {self.local_path}")

    @classmethod
    def apply(cls, *repos: 'GitRepository') -> None:
        for repo in repos:
            repo.apply()

    def apply(self) -> None:
        if self.local_path.exists():
            return

        subprocess.run(["git", "clone", self.remote, self.local_path])

    def run_in(self, cmd: Sequence[str]) -> None:
        subprocess.run(cmd, cwd=self.local_path)
