from cfgtools.files import EnvironmentFile, normalize

import utils.bat
import utils.inputrc

NAME = normalize(__name__)

files = [
    EnvironmentFile(NAME)
]
