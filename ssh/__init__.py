from pathlib import Path

from cfgtools.files import File
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

packages = {Pacman("openssh"), Apt("ssh-client")}
files = [
    File(f"{__name__}/default.ssh", Path.home() / ".ssh/config.d/default")
]


@after
def setup_base_ssh_config() -> None:
    base_config = Path.home() / ".ssh/config"
    base_config_template = Path(__file__).parent / "base.ssh"
    if not base_config.exists():
        base_config.write_text(base_config_template.read_text())
    else:
        include_line, _ = base_config_template.read_text().split('\n', 1)
        if not base_config.read_text().startswith(include_line):
            print(
                f'!!! Please add `{include_line}` to the top'
                f' of your `{base_config}` file.'
            )
