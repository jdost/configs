from cfgtools.files import EnvironmentFile, XDGConfigFile, normalize
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.ubuntu import Apt

NAME = normalize(__name__)

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
    XDGConfigFile(f"{NAME}/pip.conf", "pip/pip.conf"),
    EnvironmentFile(NAME),
    XDGConfigFile(f"{NAME}/python_startup.py", "python/startup.py"),
    XDGConfigFile(f"{NAME}/black.toml", "black"),
    XDGConfigFile(f"{NAME}/isort.cfg", "isort.cfg"),
]
