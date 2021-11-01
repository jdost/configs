from cfgtools.files import EnvironmentFile, XDGConfigFile
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.ubuntu import Apt

python_tools = [
    "black",
    "flake8",
    "isort",
    "mypy",
    "mypy-ls",
    "neovim",
    "pynvim",
    "python-lsp-black",
    "python-lsp-server",
]

packages = {
    Pacman("python"),
    Pacman("python-wheel"),
    Apt("python3"),
    Apt("python3-pip"),
    Apt("python3-venv"),
    VirtualEnv("python-code-tools", *python_tools),
}
files = [
    XDGConfigFile(f"{__name__}/pip.conf", "pip/pip.conf"),
    EnvironmentFile(__name__),
    XDGConfigFile(f"{__name__}/python_startup.py", "python/startup.py"),
    XDGConfigFile(f"{__name__}/black.toml", "black"),
    XDGConfigFile(f"{__name__}/isort.cfg", "isort.cfg"),
]
