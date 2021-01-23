import subprocess

from cfgtools.files import XDGConfigFile, XDG_CONFIG_HOME, UserBin
from cfgtools.hooks import after
from cfgtools.system import GitRepository
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService

packages={
    AUR("polybar"), AUR("./aur/pkgs/ttf-anonymous-pro-ext"),
    Pacman("python-gobject"), Pacman("noto-fonts"), Pacman("noto-fonts-emoji"),
}
systemhud_repo = GitRepository("git@github.com:jdost/systemhud.git")
systemhud_venv = VirtualEnv("systemhud", system_packages=True)
files=[
    UserService("polybar/statusbar.service"),
    XDGConfigFile(f"{__name__}/config"),
    XDGConfigFile(f"{__name__}/modules"),
]


@after
def enable_statusbar_service() -> None:
    ensure_service("statusbar", user=True)


@after
def setup_systemhud_repo() -> None:
    for installed_req in systemhud_venv.installed_requirements:
        if "jdost/systemhud.git" in installed_req:
            return

    systemhud_repo.run_in(
        [systemhud_venv.location / "bin/python", "-m", "pip", "install", "-U", "-e", "src/"]
    )

    modules_dst = XDG_CONFIG_HOME / "polybar/systemhud_modules"
    if not modules_dst.exists():
        modules_dst.symlink_to(systemhud_repo.local_path / "etc/polybar")
    global_bins = ["notify-send", "screen-brightness"]
    for global_bin in global_bins:
        src = systemhud_venv.location / "bin" / global_bin
        dst = UserBin.DIR / global_bin
        if dst.exists():
            continue
        if not src.exists():
            raise FileNotFoundError(
                f"Cannot link {src} into path, does not exist."
            )

        dst.symlink_to(src)
