from cfgtools.files import EnvironmentFile, XDGConfigFile
from cfgtools.system.arch import Pacman

packages={Pacman("python")}
files=[
    XDGConfigFile(f"{__name__}/pip.conf", "pip/pip.conf"),
    EnvironmentFile(__name__),
    XDGConfigFile(f"{__name__}/python_startup.py", "python/startup.py"),
]
