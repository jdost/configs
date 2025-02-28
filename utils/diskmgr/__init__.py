from cfgtools.files import UserBin, normalize

NAME = normalize(__name__)

files = [
    UserBin(f"{NAME}/diskmgr.py", "diskmgr"),
]
