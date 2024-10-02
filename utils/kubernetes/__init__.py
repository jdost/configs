from cfgtools.files import UserBin, normalize
from cfgtools.system.arch import Pacman

NAME = normalize(__name__)
system_packages={Pacman("helm"), Pacman("kubectl")}
files=[
    UserBin(f"{NAME}/helm-wrapper.sh", "helm"),
    UserBin(f"{NAME}/kubectl-wrapper.sh", "kubectl"),
]
