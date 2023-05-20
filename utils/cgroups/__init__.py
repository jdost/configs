from cfgtools.files import UserBin, normalize
from rofi import RofiModule

NAME = normalize(__name__)

files = [
    UserBin(f"{NAME}/run_with_cgroup.sh", "run-in-cgroup"),
    RofiModule(f"{NAME}/rofi.rasi", "cgroups"),
]
