from cfgtools.files import EnvironmentFile, XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.system.ubuntu import Apt

packages={Pacman("python"), Apt("python3"), Apt("python3-venv")}
files=[
    XDGConfigFile(f"{__name__}/pip.conf", "pip/pip.conf"),
    EnvironmentFile(__name__),
    XDGConfigFile(f"{__name__}/python_startup.py", "python/startup.py"),
]
