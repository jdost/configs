from cfgtools.files import UserBin, normalize
from cfgtools.system.python import VirtualEnv

NAME = normalize(__name__)
VirtualEnv("llm", "llm")

files = {
    UserBin(f"{NAME}/llm_wrapper.py", "llm"),
}
