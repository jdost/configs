import os
import subprocess

from pathlib import Path
from typing import Optional, Union

HOME = Path.home()
BASE = Path(__file__).resolve().parent.parent
XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))

registered_files = set()


def convert_loc(p: Union[Path, str]) -> Path:
    if not isinstance(p, Path):
        p = Path(p)

    return p if p.is_absolute() else BASE / p


class LocalConflict(Exception):
    def __init__(self, conflicting_path: Path):
        super().__init__(
            f"{conflicting_path} already exists and is not the correct type."
        )


class RegisteredFileAction:
    def __init__(self):
        registered_files.add(self)

    def __repr__(self) -> str:
        return str(self.__class__)


class File(RegisteredFileAction):
    src: Path
    dst: Path
    force: bool = False

    def __init__(self, src: Union[Path, str], dst: Union[Path, str], force: bool = False):
        self.src = convert_loc(src)
        self.dst = convert_loc(dst)
        self.force = force

        super().__init__()

    def dry_run(self) -> None:
        if not self.src.exists():
            # There is no file to be symlinked, probably a typo
            raise FileNotFoundError(self.src)

        if self.dst.exists():
            if self.dst.resolve() == self.src:
                # noop - symlink already exists
                return
            elif not self.force:
                raise LocalConflict(self.dst)
        elif self.dst.is_symlink():
            print(f"$ rm {self.dst}")

        if not self.dst.parent.exists():
            print(f"$ mkdir -p {self.dst.parent}")

        print(f"$ ln -s {self.src} {self.dst}")

    def apply(self) -> None:
        if not self.src.exists():
            # There is no file to be symlinked, probably a typo
            raise FileNotFoundError(self.src)

        if self.dst.exists():
            if self.dst.resolve() == self.src:
                # noop - symlink already exists
                return

            if self.force:
                # we want to override anything there with this symlink
                self.dst.unlink()
            else:
                raise LocalConflict(self.dst)
        elif self.dst.is_symlink():
            # `.exists` will return True for symlinks with a valid target, but
            #   will be False for bad symlinks, but they will still be symlinks
            #   so this branch of the conditional is if it is a symlink but it
            #   does not have a valid target, so we want to remove the bad ref
            #   and create a new one
            print(f"Removing bad symlink: {self.dst}")
            self.dst.unlink()

        if not self.dst.parent.exists():
            print(f"Creating parent directory: {self.dst.parent}")
            self.dst.parent.mkdir(parents=True)

        try:
            self.dst.symlink_to(self.src)
            print(f"Symlink: {self.src} -> {self.dst}")
        except PermissionError:
            print(f"Symlink (as root): {self.src} -> {self.dst}")
            subprocess.run(["sudo", "ln", "-s", str(self.src), str(self.dst)])

    def __repr__(self) -> str:
        return f"{self.__class__} {self.src} -> {self.dst}"


class EnvironmentFile(File):
    def __init__(self, src_name: str, name: Optional[str] = None):
        dst_name = name if name else src_name
        super().__init__(
            src=(BASE / src_name / "environment"),
            dst=(HOME / ".local/environment" / dst_name),
        )


class UserBin(File):
    DIR = HOME / ".local/bin"
    def __init__(self, src: Union[str, Path], name: str):
        super().__init__(src=src, dst=(UserBin.DIR / name))


class XDGConfigFile(File):
    def __init__(self, src: str, tgt: Optional[str] = None):
        #dst = f"{tgt}/{Path(src).name}" if tgt else src
        dst = tgt if tgt else src
        super().__init__(src=src, dst=XDG_CONFIG_HOME / dst)


class XinitRC(File):
    DIR = XDG_CONFIG_HOME / "xorg/xinitrc.d"
    def __init__(self, name: str, priority: int = 99):
        super().__init__(
            src=(BASE / name / "xinitrc"),
            dst=(self.DIR / f"{priority}-{name}"),
        )


class DesktopEntry(File):
    DIR = HOME / ".local/share/applications"
    def __init__(self, src: str, name: Optional[str] = None):
        filename = name if name else Path(src).name
        if not filename.endswith(".desktop"):
            filename=f"{filename}.desktop"
        super().__init__(src=src, dst=(DesktopEntry.DIR / filename))


class Folder(RegisteredFileAction):
    UNSET_PERMISSIONS = -1
    MASK=0o777

    def __init__(self, location: Path, permissions: int = UNSET_PERMISSIONS):
        self.location = location
        self.permissions = permissions

        super().__init__()

    @property
    def mod(self) -> int:
        return self.location.stat().st_mode & self.MASK

    def dry_run(self) -> None:
        if self.location.exists() and not self.location.is_dir():
            raise LocalConflict(self.location)

        if not self.location.is_dir():
            print(f"$ mkdir -p {self.location}")

        if self.permissions == Folder.UNSET_PERMISSIONS:
            return

        if self.location.exists():
            if self.mod != self.permissions:
                print(f"$ chmod {self.permissions} {self.location}")

    def apply(self) -> None:
        if self.location.exists() and not self.location.is_dir():
            raise LocalConflict(self.location)

        if not self.location.is_dir():
            self.location.mkdir(parents=True)

        if self.permissions == Folder.UNSET_PERMISSIONS:
            return

        if self.mod != self.permissions:
            self.location.chmod(self.permissions)

    def __repr__(self) -> str:
        if self.permissions != Folder.UNSET_PERMISSIONS:
            return f"{self.__class__} {self.location} ({self.permissions})"
        return f"{self.__class__} {self.location}"


def setup(dry_run: bool = False) -> None:
    global registered_files
    for file in registered_files:
        if dry_run:
            file.dry_run()
        else:
            file.apply()
