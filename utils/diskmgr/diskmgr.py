#!/usr/bin/env python3
import asyncio
import json
import os
import re
import shlex
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Dict, List, Optional, Sequence, Set, Union

FSTAB = Path("/etc/fstab")
LVM_FSTYPE = "LVM2_member"
SUDO = "/usr/bin/sudo"
DISKS_DEFINITION = Path.home() / ".local/dropbox/configs/disks.json"
IS_TERMINAL = os.environ.get("TERM") not in {"linux", None}
ASKPASS = shutil.which("rofi-askpass")


@dataclass
class VolumeGroup:
    name: str
    uuid: Optional[str] = None  # UUID is only wanted for the fstab generation

    @property
    def description(self) -> str:
        if self.uuid:
            return f"LVM VG:{self.name} (PV UUID={self.uuid})"
        else:
            return f"LVM VG:{self.name}"

    async def is_imported(self) -> bool:
        proc = await run_cmd("vgs", self.name, as_root=True)
        await proc.wait()
        return proc.returncode == 0

    async def import_vg(self) -> bool:
        if await self.is_imported():
            return True

        proc = await run_cmd("vgimport", "--yes", self.name, as_root=True)
        await proc.wait()
        return proc.returncode == 0

    async def export_vg(self) -> bool:
        if not await self.is_imported():
            return True

        proc = await run_cmd("vgexport", "--yes", self.name, as_root=True)
        await proc.wait()
        return proc.returncode == 0

    async def is_activated(self) -> bool:
        proc = await run_cmd("lvs", f"/dev/{self.name}", as_root=True)
        await proc.wait()
        return proc.returncode == 0

    async def activate_vg(self) -> bool:
        if await self.is_activated():
            return True

        proc = await run_cmd("lvchange", "--activate", "y", f"/dev/{self.name}", as_root=True)
        await proc.wait()
        return proc.returncode == 0

    async def deactivate_vg(self) -> bool:
        if not await self.is_activated():
            return True

        proc = await run_cmd("lvchange", "--activate", "n", f"/dev/{self.name}", as_root=True)
        await proc.wait()
        return proc.returncode == 0

    async def logical_volumes(self) -> Sequence["LogicalVolume"]:
        output = await json_output("lvs", "--reportformat", "json", self.name, as_root=True)

        assert "report" in output
        assert isinstance(output["report"], list)
        assert len(output["report"]) > 0

        lv_listing = output["report"][0]
        assert "lv" in lv_listing
        assert isinstance(lv_listing["lv"], list)

        return [LogicalVolume.from_lvreport(self, lv_info) for lv_info in lv_listing["lv"]]


@dataclass
class LogicalVolume:
    volume_group: VolumeGroup
    name: str

    @staticmethod
    def is_entry(entry: str) -> bool:
        return bool(
            re.match(r"^/dev/mapper/([a-zA-Z0-9-]+)-([a-zA-Z0-9-]+)$", entry)
        )

    @property
    def dev(self) -> str:
        return f"/dev/mapper/{self.volume_group.name}-{self.name}"

    @classmethod
    def from_lvreport(cls, vg: VolumeGroup, lv_info: Dict[str, Any]) -> "LogicalVolume":
        assert "lv_name" in lv_info
        assert isinstance(lv_info["lv_name"], str)
        return cls(volume_group=vg, name=lv_info["lv_name"])

    @classmethod
    def from_entry(cls, entry: str) -> "LogicalVolume":
        dev_path = Path(entry)
        vg_name, lv_name = dev_path.name.split("-", 1)
        return cls(volume_group=VolumeGroup(name=vg_name), name=lv_name)


@dataclass
class BlockDevice:
    name: str
    hotplug: bool
    fstype: str
    label: Optional[str]
    uuid: Optional[str]
    path: Path
    children: Sequence['BlockDevice']

    @property
    def has_dev(self) -> bool:
        return bool(self.fstype) or bool(self.children)

    @classmethod
    def from_cmd(cls, output: Dict[str, Any]) -> 'BlockDevice':
        for k, t in [("name", str), ("hotplug", bool), ("path", str)]:
            assert k in output, f"{k} key missing from input struct"
            assert isinstance(output[k], t), f"{k} is the wrong type, expected {t}, got {type(output[k])}"

        if "children" in output:
            assert isinstance(output["children"], list)
            children = [BlockDevice.from_cmd(c) for c in output["children"]]
        else:
            children = []

        return cls(
            name=output["name"],
            hotplug=output["hotplug"],
            fstype=output["fstype"],
            label=output.get("label"),
            uuid=output.get("uuid"),
            path=Path(output["path"]),
            children=children,
        )

    def __repr__(self) -> str:
        return f"<BlockDevice({self.name}) - {self.path}>"


@dataclass
class UUID:
    """ Simple wrapper type for UUID based device mounts.
    """
    uuid: str
    ENTRY_PREFIX = "UUID="

    @property
    def dev(self) -> str:
        return f"{UUID.ENTRY_PREFIX}{self.uuid}"

    @classmethod
    def is_entry(cls, entry: str) -> bool:
        return entry.startswith(cls.ENTRY_PREFIX)

    @classmethod
    def from_entry(cls, entry: str) -> 'UUID':
        return cls(uuid=entry[len(UUID.ENTRY_PREFIX):])


@dataclass
class Mount:
    """ Mount is a singular entry in the fstab that is just an entry
    of a device (under `/dev/...`) to a point in the local FS along with
    information for how to mount that device to that point.
    """
    source: Union[UUID, LogicalVolume]
    mountpoint: Path
    fstype: str = "ext4"
    options: Sequence[str] = ("rw", "noauto", "user", "exec")
    dump: int = 0
    fsck: int = 2

    def __repr__(self) -> str:
        return f"<Mount({self.mountpoint}) source={self.source.dev}>"

    def ensure_exists(self) -> None:
        """ Create the local mountpoint directory locally."""
        if self.mountpoint.expanduser().exists():
            return

        self.mountpoint.expanduser().mkdir(parents=True, exist_ok=True)

    def as_entry(self) -> Sequence[str]:
        """ Column split of the fstab entry:
            > <source>   <local mount>   <fstype>   <options>   <dump>   <fsck>
        """
        return [
            # This is the device definition for the source, handled by the
            #   type wrapper
            self.source.dev,
            # This is the path in the local fs to mount to
            str(self.mountpoint.expanduser()),
            self.fstype,  # This is the filesystem to mount as
            ",".join(self.options),  # Options for the mount
            str(self.dump),  # Whether to check with the dump util
            str(self.fsck),  # Order to check the disk on boot
        ]

    @classmethod
    def from_entry(cls, entry_line: str) -> Optional["Mount"]:
        raw_source, mountpoint, fstype, options, dump, fsck = entry_line.split()
        source: Union[UUID, LogicalVolume, None] = None
        if UUID.is_entry(raw_source):
            source = UUID.from_entry(raw_source)
        elif LogicalVolume.is_entry(raw_source):
            source = LogicalVolume.from_entry(raw_source)

        if source is None:
            return None

        return cls(
            source=source,
            mountpoint=Path(mountpoint),
            fstype=fstype,
            options=options.split(","),
            dump=int(dump),
            fsck=int(fsck),
        )

    def __hash__(self) -> int:
        return hash(" ".join(self.as_entry()))


@dataclass
class MountGroup:
    """ MountGroup: A collection of mount entries in the fstab
    that correspond to a singular storage device (typically a removable
    storage) of some type.
    """
    name: str
    mounts: Set[Mount]
    description: Optional[str] = None

    @property
    def header(self) -> str:
        lines = [f"# {self.name}"]
        if self.description:
            lines.append(f"#   {self.description}")

        return "\n".join(lines)


    def fstab_entry(self) -> Sequence[str]:
        """The fstab entry is a comment header to describe the group, then
        columnized listings of each mount entry for the group.  We want the
        header to be unique so we can find previously generated groups.
        """
        # The mount listing generation is done in two passes...
        mount_entries = [m.as_entry() for m in self.mounts]
        # The first is calculating the column widths, which we use a format
        #   string to control, this ends up just being a sequence of :
        #   > {index:<column_width}
        #   where index describes which column, then `:<` is a left aligned
        #   string with a right padding to `column_width` length
        format_str = ""
        for i in range(len(mount_entries[0])):
            width = max([len(mount[i]) for mount in mount_entries])
            format_str += f"{{{i}:<{width}}}    "
        # The second pass then just pushes each row into the column aligned
        #   format string
        mount_str = [format_str.format(*e) for e in mount_entries]
        # Then we include the comment header along with a consistent ordering
        #   of the formatted mount lines
        return [self.header, *sorted(mount_str)]


async def check_sudo() -> None:
    uptime_bin = shutil.which("uptime")
    assert uptime_bin is not None, "No idea why you don't have uptime"

    test_proc = await asyncio.subprocess.create_subprocess_exec(
        SUDO, "--non-interactive", uptime_bin,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await test_proc.wait()
    if test_proc.returncode == 0:
        return

    if not IS_TERMINAL:
        if ASKPASS is None:
            print("You need a GUI based prompt...")
            sys.exit(1)

        grant_proc = await asyncio.subprocess.create_subprocess_exec(
            SUDO, "-A", "--prompt=Need root privileges for commands", uptime_bin,
            stdout=asyncio.subprocess.DEVNULL,
            env={"SUDO_ASKPASS": ASKPASS, **os.environ},
        )
    else:
        print("Need root privileges for commands, enter password")
        grant_proc = await asyncio.subprocess.create_subprocess_exec(
            SUDO, uptime_bin,
            stdout=asyncio.subprocess.DEVNULL,
        )

    await grant_proc.wait()
    assert grant_proc.returncode == 0, "sudo not granted"


async def run_cmd(binary, *args, as_root: bool = False) -> asyncio.subprocess.Process:
    executable = shutil.which(binary)
    if executable is None:
        print(f"There is no valid executable for {binary}")
        return sys.exit(1)

    if as_root:
        await check_sudo()

    cmd = [SUDO, executable, *args] if as_root else [executable, *args]
    print(shlex.join(cmd))
    return await asyncio.subprocess.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )


async def json_output(binary, *cmd, as_root: bool = False) -> Dict[str, Any]:
    proc = await run_cmd(binary, *cmd, as_root=as_root)
    stdout, _ = await proc.communicate()
    parsed = json.loads(stdout.decode())
    assert isinstance(parsed, dict), "Unexpected JSON parsed type"
    return parsed


async def get_block_devices() -> Sequence[BlockDevice]:
    lsblk_path = shutil.which("lsblk")
    assert lsblk_path is not None, "lsblk not installed into path"

    parsed_output = await json_output(
        lsblk_path,
        "--output",
        ",".join(["NAME", "FSTYPE", "HOTPLUG", "LABEL", "UUID", "PATH"]),
        "--json",
    )

    return [BlockDevice.from_cmd(d) for d in parsed_output["blockdevices"]]


def get_fstab_entries() -> Collection[Mount]:
    mounts = set()
    for raw_line in FSTAB.read_text().split("\n"):
        line = raw_line.strip()
        # Skip comment lines
        if line.startswith("#"):
            continue
        # Skip blank lines
        if len(line) == 0:
            continue

        mount = Mount.from_entry(line)
        if mount:
            mounts.add(mount)

    return mounts


async def mount(block_device: Union[str, Path]) -> bool:
    device_to_mount_mapping = {m.source.dev: m for m in get_fstab_entries()}
    if str(block_device) not in device_to_mount_mapping:
        print(f"No fstab entry for {block_device}, skipping")
        return False

    mount = device_to_mount_mapping[str(block_device)]
    if not mount.mountpoint.exists():
        print(f"The target mountpoint for {block_device} does not exist: {mount.mountpoint}")
        return False

    # Already a mount point, means it's already mounted so no-op
    if mount.mountpoint.is_mount():
        return True

    proc = await run_cmd(
        "/usr/bin/mount", str(mount.mountpoint),
        as_root=("user" not in set(mount.options))
    )
    await proc.wait()
    return proc.returncode == 0


async def umount(block_device: Union[str, Path]) -> bool:
    device_to_mount_mapping = {m.source.dev: m for m in get_fstab_entries()}
    if str(block_device) not in device_to_mount_mapping:
        print(f"No fstab entry for {block_device}, skipping")
        return False

    mount = device_to_mount_mapping[str(block_device)]
    if not mount.mountpoint.exists():
        print(f"The target mountpoint for {block_device} does not exist: {mount.mountpoint}")
        return False

    # Not a mount point, probably means it's already unmounted
    if not mount.mountpoint.is_mount():
        return True

    proc = await run_cmd(
        "/usr/bin/umount", str(mount.mountpoint),
        as_root=("user" not in set(mount.options))
    )
    await proc.wait()
    return proc.returncode == 0


async def get_volumegroup(device: Union[str, Path]) -> Optional[VolumeGroup]:
    output = await json_output("pvs", "--reportformat", "json", str(device), as_root=True)

    assert "report" in output
    assert isinstance(output["report"], list)
    assert len(output["report"]) > 0
    assert "pv" in output["report"][0]
    pv_output = output["report"][0]["pv"]

    assert isinstance(pv_output, list)
    assert len(pv_output) > 0

    pv_info = pv_output[0]
    if pv_info.get("pv_name") != str(device):
        return None

    return VolumeGroup(name=pv_info.get("vg_name"))


def gen_fstab() -> None:
    disks = json.load(DISKS_DEFINITION.open())
    print("The lines to be added to /etc/fstab:")
    for identifier in disks.keys():
        disk = disks[identifier]
        if disk["type"] == "lvm":
            vg = VolumeGroup(name=disk["name"], uuid=identifier)
            mounts: List[Mount] = []

            for logical_volume in disk["submounts"]:
                lv = LogicalVolume(volume_group=vg, name=logical_volume)
                mounts.append(Mount(source=lv, mountpoint=Path(disk["submounts"][logical_volume])))

            mount_group = MountGroup(
                name=disk["device"],
                description=vg.description,
                mounts=set(mounts),
            )

            print("\n".join(mount_group.fstab_entry()))

        print("")


async def mount_cmd(dev_path: str) -> bool:
    target = (
        Path(dev_path) if dev_path.startswith("/dev")
        else Path(f"/dev/{dev_path}")
    )

    devs = await get_block_devices()
    block_device: Optional[BlockDevice] = None
    for d in devs:
        if d.path == target:
            block_device = d
            break

    if not block_device:
        print(f"No available block device for {target}")
        return sys.exit(1)

    defined_device = json.load(DISKS_DEFINITION.open()).get(block_device.uuid)
    if defined_device is None:
        print(f"The target device isn't a pre-defined target: {block_device.uuid}")
        return sys.exit(2)

    if block_device.fstype == LVM_FSTYPE:
        # This is an LVM based block device, we need to handle this a bit
        #   differently
        vg = await get_volumegroup(block_device.path)
        if not vg:
            print(f"There is no volume group for {block_device.path}")
            return sys.exit(3)
        await vg.import_vg()
        await vg.activate_vg()
        for lv in await vg.logical_volumes():
            await mount(lv.dev)

    return True


async def unmount_cmd(dev_path: str) -> bool:
    target = (
        Path(dev_path) if dev_path.startswith("/dev")
        else Path(f"/dev/{dev_path}")
    )

    devs = await get_block_devices()
    block_device: Optional[BlockDevice] = None
    for d in devs:
        if d.path == target:
            block_device = d
            break

    if not block_device:
        print(f"No available block device for {target}")
        return sys.exit(1)

    if block_device.fstype == LVM_FSTYPE:
        # This is an LVM based block device, we need to handle this a bit
        #   differently
        vg = await get_volumegroup(block_device.path)
        if not vg:
            print(f"There is no volume group for {block_device.path}")
            return sys.exit(3)

        for lv in await vg.logical_volumes():
            await umount(lv.dev)

        await vg.deactivate_vg()
        await vg.export_vg()

    return True


def main():
    if len(sys.argv) == 1:
        print("Provide a subcommand, options are:")
        print("  gen-fstab/fstab, mount/mnt, unmount/unmt/umount")
        sys.exit(1)
    if sys.argv[1] in {"gen-fstab", "fstab"}:
        gen_fstab()
    elif sys.argv[1] in {"mount", "mnt"}:
        assert len(sys.argv) > 2, "Need to provide a device to mount..."
        asyncio.run(mount_cmd(sys.argv[2]))
    elif sys.argv[1] in {"unmount", "umnt", "umount"}:
        assert len(sys.argv) > 2, "Need to provide a device to unmount..."
        asyncio.run(unmount_cmd(sys.argv[2]))
    else:
        print(f"Unknown subcommand: {sys.argv[1]}")
        sys.exit(1)

if __name__ == "__main__":
    main()
