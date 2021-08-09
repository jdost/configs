import shutil
import subprocess
import urllib.request as urllib
from tempfile import NamedTemporaryFile
from typing import Set

from cfgtools.system import SystemPackage
from cfgtools.utils import cmd_output

IS_UBUNTU = (
    shutil.which("lsb_release") is not None
    and cmd_output("lsb_release -i")[0] == "Distributor ID:	Ubuntu"
)


def installed_packages() -> Set[str]:
    return {pkg for pkg in cmd_output("dpkg-query -W --showformat='${Package}\n'")}


class Apt(SystemPackage):
    def __init__(self, name: str):
        self.name = name
        if IS_UBUNTU:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    @classmethod
    def dry_run(cls, *pkgs: "Apt") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_packages()
        if to_be_installed:
            print(
                "# apt-get install --no-install-recommends -y "
                f"{' '.join(list(to_be_installed))}"
            )

    @classmethod
    def apply(cls, *pkgs: "Apt") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_packages()
        if to_be_installed:
            print(f"Installing (apt-get): {', '.join(list(to_be_installed))}")
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "--no-install-recommends"]
                + list(to_be_installed)
            )


class Deb(SystemPackage):
    PRIORITY = 2

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        if IS_UBUNTU:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name} ({self.url})"

    @classmethod
    def dry_run(cls, *pkgs: "Deb") -> None:
        wanted = {pkg.name: pkg for pkg in pkgs}
        to_be_installed = set(wanted.keys()) - installed_packages()
        if to_be_installed:
            for pkg_name in to_be_installed:
                wanted[pkg_name]._dry_run()

    def _dry_run(self) -> None:
        print(
            f"# curl -o {self.name}.deb {self.url}" f" && sudo dpkg -i {self.name}.deb"
        )

    @classmethod
    def apply(cls, *pkgs: "Deb") -> None:
        wanted = {pkg.name: pkg for pkg in pkgs}
        to_be_installed = set(wanted.keys()) - installed_packages()
        if to_be_installed:
            for pkg_name in to_be_installed:
                wanted[pkg_name]._apply()

    def _apply(self) -> None:
        with NamedTemporaryFile(suffix=".deb") as deb, urllib.urlopen(
            self.url
        ) as src_file:
            shutil.copyfileobj(src_file, deb)
            subprocess.run(["sudo", "dpkg", "-i", deb.name])
