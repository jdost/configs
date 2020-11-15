import subprocess

from pathlib import Path
from typing import Set, Sequence

from cfgtools.system import SystemPackage


class VirtualEnv(SystemPackage):
    BASE_LOCATION = Path.home() / ".local"

    def __init__(self, name: str, *requirements: str, system_packages: bool = False):
        self.name = name
        self.requirements = set(requirements)
        self.system_packages = system_packages
        super().__init__()

    @property
    def location(self) -> Path:
        return VirtualEnv.BASE_LOCATION / self.name

    @classmethod
    def dry_run(cls, *pkgs: 'VirtualEnv') -> None:
        for pkg in pkgs:
            pkg.dry_run()

    @property
    def installed_requirements(self) -> Set[str]:
        if not self.location.exists():
            return set()

        return {
            req.split("=")[0] for req in
            subprocess.run(
                [self.location / "bin/python", "-m", "pip", "freeze"],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8").split("\n")
        }

    @property
    def venv_cmd(self) -> Sequence[str]:
        cmd = ["python", "-m", "venv"]
        if self.system_packages:
            cmd.append("--system-site-packages")
        cmd += ["--prompt", f"({self.name})"]
        cmd += [str(self.location)]

        return cmd

    def dry_run(self) -> None:
        if not self.location.exists():
            print(f"$ {' '.join(self.venv_cmd)}")
            print(
                f"$ {self.location}/bin/python -m pip install "
                ' '.join(self.requirements)
            )
        else:
            uninstalled = self.requirements - self.installed_requirements
            if uninstalled:
                print(
                    f"$ {self.location}/bin/python -m pip install "
                    ' '.join(uninstalled)
                )

    @classmethod
    def apply(cls, *pkgs: 'VirtualEnv') -> None:
        for pkg in pkgs:
            pkg.apply()

    def apply(self) -> None:
        if not self.location.exists():
            if not self.location.parent.exists():
                self.location.parent.mkdir(parents=True)

            subprocess.run(self.venv_cmd)

        uninstalled = self.requirements - self.installed_requirements
        if uninstalled:
            subprocess.run(
                [self.location / "bin/python", "-m", "pip", "install"] \
                + list(uninstalled)
            )
