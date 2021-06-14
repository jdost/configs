import shutil
import subprocess

from typing import Set

from cfgtools.system import SystemPackage
from cfgtools.utils import cmd_output

IS_UBUNTU = shutil.which("lsb_release") != None and \
    cmd_output("lsb_release -i")[0] == "Distributor ID:	Ubuntu"


def installed_pkgs() -> Set[str]:
    return {
        pkg for pkg in cmd_output("dpkg-query -W --showformat='${Package}'\n")
    }


class Apt(SystemPackage):
    def __init__(self, name: str):
        self.name = name
        if IS_UBUNTU:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    @classmethod
    def dry_run(cls, *pkgs: 'Apt') -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(
                "# apt-get install --no-install-recommends -y "
                f"{' '.join(list(to_be_installed))}"
            )

    @classmethod
    def apply(cls, *pkgs: 'Apt') -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(f"Installing (apt-get): {', '.join(list(to_be_installed))}")
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "--no-install-recommends"] +
                list(to_be_installed)
            )
