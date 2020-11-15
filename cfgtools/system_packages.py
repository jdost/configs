import abc
from collections import defaultdict


class SystemPackage:
    collection = set()

    def __new__(cls, *args, **kwargs):
        obj = super(SystemPackage, cls).__init__(*args, **kwargs)
        cls.collection.add(obj)
        return obj


class SystemPackageCollector:
    def __init__(self):
        self.pkgs = defaultdict(set)

    def add(self, pkg: SystemPackage) -> None:
        if not pkg.check(pkg):
            self.pkgs[pkg.__class__.__name__].add(pkg)

    def install(self) -> None:
        for _, pkgs in self.pkgs.items():
            pkgs[0].install(*pkgs)
