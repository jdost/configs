from cfgtools.files import XDGConfigFile, normalize

NAME = normalize(__name__)

files = [
    XDGConfigFile(f"{NAME}/ackrc", "ackrc"),
]
