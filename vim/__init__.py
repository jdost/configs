from cfgtools.files import EnvironmentFile, UserBin, XDGConfigFile, normalize
from cfgtools.hooks import after
from cfgtools.system.arch import Pacman
from cfgtools.system.nix import NixPkgBin

NAME = normalize(__name__)
CONFIG_FILES = ["vimrc", "ftplugin", "plugin", "plugins.vim"]
VIM_PLUG_URL = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"

packages={
    Pacman("neovim"), Pacman("python-pynvim"),
    NixPkgBin("neovim"),
}
files=[
    EnvironmentFile(NAME),
    UserBin(f"{NAME}/wrapper.sh", "vim"),
    XDGConfigFile("vim/neovim.vim", "nvim/init.vim"),
] + [XDGConfigFile(f"{NAME}/{f}") for f in CONFIG_FILES]


@after
def grab_vimplug() -> None:
    """
    On initial setup, vim-plug doesn't exist and it fails to auto load from the
    vimscript, so we grab it here if it isn't there.
    """
    vim_plug_loc = XDGConfigFile.DIR / "vim/autoload/plug.vim"
    if vim_plug_loc.exists():
        return

    import urllib.request

    vim_plug_loc.parent.mkdir(exist_ok=True, parents=True)
    with urllib.request.urlopen(VIM_PLUG_URL) as req:
        vim_plug_loc.write_text(req.read().decode())
