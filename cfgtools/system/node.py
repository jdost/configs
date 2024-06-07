import json
import subprocess

from typing import Set

from cfgtools.system import SystemPackage


def installed_pkgs() -> Set[str]:
    return set(json.loads(
            subprocess.run(
                ["npm", "-g", "list", "--json"],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
        )["dependencies"].keys()
    )


class NodePackage(SystemPackage):
    PRIORITY = 3

    def __init__(self, pkg: str):
        self.name = pkg
        super().__init__()

    @classmethod
    def dry_run(cls, *pkgs: "NodePackage") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(
                "$ npm install --global "
                f"{' '.join(list(to_be_installed))}"
            )

    @classmethod
    def apply(cls, *pkgs: "NodePackage") -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs()
        if to_be_installed:
            print(f"Installing (npm): {', '.join(list(to_be_installed))}")
            subprocess.run(
                ["npm", "install", "--global", *list(to_be_installed)]
            )
