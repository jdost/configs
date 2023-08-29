import homebin
from cfgtools.files import UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.systemd import ensure_service
from cfgtools.system.ubuntu import Apt
from cfgtools.utils import add_group

NAME = normalize(__name__)

system_packages = {
    Pacman("docker"), Pacman("docker-buildx"), Apt("docker.io")
}
files = [
    UserBin(f"{NAME}/wrapper.sh", "docker"),
    XDGConfigFile(f"{NAME}/config.json", "docker/config.json"),
]

@after
def start_docker_service() -> None:
    ensure_service("docker.service")


@after
def give_user_docker_access() -> None:
    add_group("docker")
