from cfgtools.files import UserBin
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt
from cfgtools.system.systemd import ensure_service
from cfgtools.utils import add_group

import homebin

system_packages={Pacman("docker"), Apt("docker.io")}
files=[
    UserBin("docker/wrapper.sh", "docker")
]

@after
def start_docker_service() -> None:
    ensure_service("docker.service")


@after
def give_user_docker_access() -> None:
    add_group("docker")
