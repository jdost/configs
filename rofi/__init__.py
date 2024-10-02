from pathlib import Path
from typing import List

from cfgtools.files import File, InputType, UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import AUR
from cfgtools.utils import hide_xdg_entry

NAME = normalize(__name__)

packages = {AUR("./aur/pkgs/ttf-hack-ext")}
files = [
    XDGConfigFile(f"{NAME}/config.rasi"),
    XDGConfigFile(f"{NAME}/themes/icons_launcher.rasi"),
    XDGConfigFile(f"{NAME}/themes/askpass.rasi"),
    UserBin(f"{NAME}/askpass.sh", "rofi-askpass"),
]

class RofiModule(File):
    config_dir: Path = XDGConfigFile.DIR / "rofi/config.d"

    def __init__(self, src: InputType, name: str):
        super().__init__(src=src, dst=RofiModule.config_dir / f"{name}.rasi")


@after
def build_configd_file() -> None:
    contents: List[str] = []
    rofi_config_dir = XDGConfigFile.DIR / "rofi"

    if not RofiModule.config_dir.is_dir():
        return

    for f in RofiModule.config_dir.iterdir():
        if f.is_file():
            contents.append(
                f"@import \"{str(f.relative_to(rofi_config_dir))[:-5]}\""
            )

    (rofi_config_dir / "config.d.rasi").write_text("\n".join(contents))



@after
def hide_unwanted_rofi_entries() -> None:
    [hide_xdg_entry(e) for e in ["rofi", "rofi-theme-selector"]]
