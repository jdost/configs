from cfgtools.files import File, HOME, normalize

import utils.inputrc

NAME = normalize(__name__)

files = [
    File(f"{NAME}/bashrc", HOME / ".bashrc"),
]
