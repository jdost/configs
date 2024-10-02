import shutil
import subprocess
from pathlib import Path
from typing import Optional, Set

from cfgtools.files import UserBin
from cfgtools.system import SystemPackage
from cfgtools.utils import bins, cmd_output

HAS_NIX = shutil.which("nix-env") != None
NIX_PROFILE = Path.home() / ".nix-profile"
NIXPKGS_CHANNEL = "https://github.com/NixOS/nixpkgs/archive/refs/tags/21.05.tar.gz"


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
                f"# nix-env --file {NIXPKGS_CHANNEL} " +
                ' '.join(f"--install {pkg}" for pkg in to_be_installed)
            )

    @classmethod
    def apply(cls, *pkgs: 'NixPkgBin') -> None:
        wanted = {pkg.name: pkg for pkg in pkgs}
        to_be_installed = set(wanted) - installed_pkgs() - bins()
        if to_be_installed:
            print(f"Installing (nix-env): {', '.join(list(to_be_installed))}")
            cmd = ["nix-env", "--file", NIXPKGS_CHANNEL]
            for pkg in to_be_installed:
                cmd.extend(["--install", pkg])

            subprocess.run(cmd)

        # Skip the out of profile symlinks if the destination doesn't exist
        if not UserBin.DIR.exists():
            return

        # We want to preserve the bins outside the profile in case that gets
        # manipulated
        for pkg_name in to_be_installed:
            bin_name = wanted[pkg_name].bin_name
            tgt = UserBin.DIR / bin_name
            src = NIX_PROFILE / f"bin/{bin_name}"
            if not tgt.exists() and src.exists():
                tgt.symlink_to(src.resolve())
