from cfgtools.files import UserProfile, normalize

NAME = normalize(__name__)

files = [
    UserProfile(NAME)
]
