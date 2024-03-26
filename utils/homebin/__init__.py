from cfgtools.files import HOME, Folder, UserBin, EnvironmentFile, normalize

NAME = normalize(__name__)

files = [
    Folder(HOME / ".local/bin", permissions=0o755),
    EnvironmentFile(NAME),
    UserBin(f"{NAME}/settitle.sh", "settitle"),
    UserBin(f"{NAME}/term_info.sh", "term-info"),
    UserBin(f"{NAME}/retry.sh", "retry"),
    UserBin(f"{NAME}/reset.sh", "reset"),
]
