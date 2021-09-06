import subprocess

from pathlib import Path

from cfgtools.files import File, XDG_CONFIG_HOME
from cfgtools.utils import cmd_output


class UserService(File):
    def __init__(self, src: str):
        service_name = Path(src).name
        super().__init__(
            src=src, dst=(XDG_CONFIG_HOME / f"systemd/user/{service_name}")
        )


def ensure_service(service_name: str, user: bool = False) -> None:
    if user:
        if cmd_output(
            f"systemctl --user is-enabled {service_name}"
        )[0] == "enabled":
            return

        print(f"Enabling user systemd service: {service_name}")
        subprocess.run(
            ["systemctl", "--user", "enable", "--now", service_name]
        )
    else:
        if cmd_output(
            f"systemctl is-enabled {service_name}"
        )[0] == "enabled":
            return

        print(f"Enabling systemd service: {service_name}")
        subprocess.run(["sudo", "systemctl", "enable", "--now", service_name])
