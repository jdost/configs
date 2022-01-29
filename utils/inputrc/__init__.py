from cfgtools.files import EnvironmentFile, XDGConfigFile, normalize

NAME = normalize(__name__)

files = [
    XDGConfigFile(f"{NAME}/inputrc", "inputrc"),
    EnvironmentFile(NAME, "inputrc"),
]
