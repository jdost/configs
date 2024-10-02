import sys
from importlib import __import__

from cfgtools import files, hooks, system

if __name__ == "__main__":
    dry_run = False
    for pkg in sys.argv[1:]:
        if pkg == "--dry-run":
            dry_run = True
            continue

        __import__(pkg)

    hooks.run_before(dry_run)
    system.setup(dry_run)
    files.setup(dry_run)
    hooks.run_after(dry_run)
