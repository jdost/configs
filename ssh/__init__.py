import urllib.request
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
        include_line, _ = base_config_template.read_text().split("\n", 1)
        if not base_config.read_text().startswith(include_line):
            print(
                f"!!! Please add `{include_line}` to the top"
                f" of your `{base_config}` file."
            )

@after
def populate_ssh_authorized_keys() -> None:
    authorized_keys = Path.home() / ".ssh/authorized_keys"
    authorized_keys_perms = 0o644

    if not authorized_keys.exists():
        print(f"Populating {authorized_keys} with github associated keys...")
        with urllib.request.urlopen("https://github.com/jdost.keys") as req:
            authorized_keys.write_text(req.read().decode())
            authorized_keys.chmod(authorized_keys_perms)
    elif (authorized_keys.stat().st_mode & 0o777) != authorized_keys_perms:
        print("!!! Your existing ssh authorized_keys file has bad permissions")
        print(
            f"!!! run `chmod {oct(authorized_keys_perms)[2:]} "
            f"{authorized_keys}` to fix!"
        )
