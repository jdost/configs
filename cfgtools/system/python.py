import subprocess
from pathlib import Path
from typing import Optional, Sequence, Set, Union

from cfgtools.system import SystemPackage


def installed_pkgs(virtualenv: Optional[Path] = None) -> Set[str]:
    pybin: Union[str, Path] = (
        virtualenv / "bin/python" if virtualenv else "python3"
    )
    return {
        req.split("=")[0]
        for req in subprocess.run(
            [pybin, "-m", "pip", "freeze"],
            stdout=subprocess.PIPE,
        )
        .stdout.decode("utf-8")
        .split("\n")
    }


class VirtualEnv(SystemPackage):
    PRIORITY = 3
    BASE_LOCATION = Path.home() / ".local"

    def __init__(self, name: str, *requirements: str):
        self.name = name
        self.requirements = set(requirements)
        super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}: {' '.join(self.requirements)}"

    @property
    def location(self) -> Path:
        return VirtualEnv.BASE_LOCATION / self.name

    @property
    def installed_requirements(self) -> Set[str]:
        if not self.location.exists():
            return set()

        return installed_pkgs(self.location)

    @property
    def venv_cmd(self) -> Sequence[str]:
        cmd = ["python", "-m", "venv", "--system-site-packages"]
        cmd += ["--prompt", f"({self.name})"]
        cmd += [str(self.location)]

        return cmd

    @classmethod
    def dry_run(cls, *pkgs: "VirtualEnv") -> None:
        for pkg in pkgs:
            pkg._dry_run()

    def _dry_run(self) -> None:
        if not self.location.exists():
            print(f"$ {' '.join(self.venv_cmd)}")
            print(
                f"$ {self.location}/bin/python -m pip install "
                f"{' '.join(self.requirements)}"
            )
        else:
            uninstalled = self.requirements - self.installed_requirements
            if uninstalled:
                print(
                    f"$ {self.location}/bin/python -m pip install "
                    f"{' '.join(uninstalled)}"
                )

    @classmethod
    def apply(cls, *pkgs: "VirtualEnv") -> None:
        for pkg in pkgs:
            pkg._apply()

    def _apply(self) -> None:
        if not self.location.exists():
            if not self.location.parent.exists():
                self.location.parent.mkdir(parents=True)

            print(f"Creating VirtualEnv: {self.location}")
            subprocess.run(self.venv_cmd)

        uninstalled: Set[str] = self.requirements - self.installed_requirements
        if uninstalled:
            print(f"Installing (virtualenv): {', '.join(list(uninstalled))}")
            bin: Path = self.location / "bin/python"
            subprocess.run([bin, "-m", "pip", "install"] + list(uninstalled))


class PythonPackage(SystemPackage):
    PRIORITY = 3

    def __init__(self, pkg: str):
        self.name = pkg
        super().__init__()

    @classmethod
    def dry_run(cls, *pkgs: "PythonPackage") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(
                "$ python3 -m pip install --user "
                f"{' '.join(list(to_be_installed))}"
            )

    @classmethod
    def apply(cls, *pkgs: "PythonPackage") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(f"Installing (pip): {', '.join(list(to_be_installed))}")
            subprocess.run(
                ["python3", "-m", "pip", "install", "--user"]
                + list(to_be_installed)
            )
