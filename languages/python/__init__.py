from cfgtools.files import EnvironmentFile, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.python import VirtualEnv
from cfgtools.system.ubuntu import Apt

NAME = normalize(__name__)

python_tools = [
    "black",
    "ruff",
    "isort",
    "mypy",
    "neovim",
    "pylsp-mypy",
    "pynvim",
    "python-lsp-black",
    "python-lsp-ruff",
    "python-lsp-server",
]

virtualenv = VirtualEnv("python-code-tools", *python_tools)
packages = {
    Pacman("python"),
    Pacman("python-pip"),
    Pacman("python-pipx"),
    Pacman("python-poetry"),
    Pacman("python-wheel"),
    Apt("python3"),
    Apt("python3-pip"),
    Apt("python3-venv"),
    virtualenv,
}
files = [
    XDGConfigFile(f"{NAME}/pip.conf", "pip/pip.conf"),
    EnvironmentFile(NAME, "python"),
    XDGConfigFile(f"{NAME}/python_startup.py", "python/startup.py"),
    XDGConfigFile(f"{NAME}/black.toml", "black"),
    XDGConfigFile(f"{NAME}/isort.cfg", "isort.cfg"),
]


@after
def create_update_script() -> None:
    """
    Write a simple update script that will upgrade the code-tools python
    packages easily.
    """
    update_script = virtualenv.location / "bin/update_pkgs"
    update_script.write_text(f"""#!/usr/bin/env bash

set -euo pipefail

exec {virtualenv.location / 'bin/python'} -m pip install --upgrade \
{' '.join(python_tools)} pip
""")
    update_script.chmod(0o744)
