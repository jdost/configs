from typing import Optional

from cfgtools.files import File, XDGConfigFile, XDG_CONFIG_HOME, UserBin, normalize
from cfgtools.hooks import after, before
from cfgtools.system import GitRepository
from cfgtools.system.arch import AUR, Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.systemd import ensure_service, UserService

NAME = normalize(__name__)

packages={
    AUR("polybar"), AUR("./aur/pkgs/ttf-anonymous-pro-ext"),
    Pacman("python-gobject"), Pacman("noto-fonts"), Pacman("noto-fonts-emoji"),
}
systemhud_repo = GitRepository("git@github.com:jdost/systemhud.git")
systemhud_venv = VirtualEnv("systemhud")
files=[
    UserService("polybar/statusbar.service"),
    XDGConfigFile(f"{NAME}/config"),
    XDGConfigFile(f"{NAME}/modules"),
]


ICON_FONT: Optional[str] = None

def set_icon_font(choice: str) -> None:
    global ICON_FONT
    ICON_FONT = choice

    from importlib import __import__
    __import__(f"polybar.icon_fonts.{choice}")


@before
def check_icon_font_set() -> None:
    global ICON_FONT
    if ICON_FONT is None:
        set_icon_font("material")


@after
def enable_statusbar_service() -> None:
    ensure_service("statusbar", user=True)


@after
def setup_systemhud_repo() -> None:
    installed = False
    for installed_req in systemhud_venv.installed_requirements:
        if "jdost/systemhud.git" in installed_req:
            installed = True

    if not installed:
        systemhud_repo.run_in(
            [systemhud_venv.location / "bin/python", "-m", "pip", "install", "-U", "-e", "src/"]
        )

    File(
        systemhud_repo.local_path / "etc/polybar",
        XDG_CONFIG_HOME / "polybar/systemhud_modules",
    ).apply()

    for global_bin in ["notify-send", "screen-brightness"]:
        File(
            systemhud_venv.location / "bin" / global_bin,
            UserBin.DIR / global_bin,
        ).apply()
