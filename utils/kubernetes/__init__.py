from cfgtools.files import UserBin
from cfgtools.system.arch import Pacman

system_packages={Pacman("helm"), Pacman("kubectl")}
files=[
    UserBin("kubernetes/helm-wrapper.sh", "helm"),
    UserBin("kubernetes/kubectl-wrapper.sh", "kubectl"),
]
