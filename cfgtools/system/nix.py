import shutil

from pathlib import Path
from typing import Optional, Set

from cfgtools.files import UserBin
from cfgtools.system import SystemPackage
from cfgtools.utils import bins, cmd_output

HAS_NIX = shutil.which("nix-env") != None
NIX_PROFILE = Path.home() / ".nix-profile"


def installed_pkgs() -> Set[str]:
    return {
        pkg.split('-', 1)[0] for pkg in cmd_output("nix-env --query")
    }


class NixPkgBin(SystemPackage):
    PRIORITY=3
    def __init__(self, name: str, bin: Optional[str] = None):
        self.name = name
        self.bin_name = bin if bin is not None else self.name
        if HAS_NIX:
            super().__init__()

    def __repr__(self):
        return f"{self.__class__} {self.name}"

    @classmethod
    def dry_run(cls, *pkgs: 'NixPkgBin') -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs() - bins()
        if to_be_installed:
            print(
                "# nix-env " +
                ' '.join(f"--install {pkg}" for pkg in to_be_installed)
            )

    @classmethod
    def apply(cls, *pkgs: 'NixPkgBin') -> None:
        wanted = {pkg.name for pkg in pkgs}
        to_be_installed = wanted - installed_pkgs() - bins()
        if to_be_installed:
            print(f"Installed (nix-env): {', '.join(list(to_be_installed))}")
            cmd = ["nix-env"]
            for pkg in to_be_installed:
                cmd.extend(["--install", pkg])

            subprocess.run(cmd)

        # We want to preserve the bins outside the profile in case that gets
        # manipulated
        for pkg_name in to_be_installed:
            bin_name = pkgs[pkg_name]
            (UserBin.DIR / bin_name).symlink_to(
                (NIX_PROFILE / "bin" / bin_name).resolve()
            )
