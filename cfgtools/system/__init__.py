from collections import defaultdict

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
