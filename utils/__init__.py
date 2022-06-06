from cfgtools.files import EnvironmentFile, normalize

NAME = normalize(__name__)

files = [
    EnvironmentFile(NAME)
]
