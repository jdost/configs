# Adblocking/Privacy
c.content.blocking.adblock.lists = [
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
    "https://easylist.to/easylist/fanboy-social.txt",
    "https://secure.fanboy.co.nz/fanboy-annoyance.txt",
    # uBlock Origin
    "https://github.com/uBlockOrigin/uAssets/raw/refs/heads/master/filters/legacy.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/refs/heads/master/filters/privacy.txt",
    "https://github.com/uBlockOrigin/uAssets/raw/refs/heads/master/filters/filters.txt",
]
c.content.blocking.enabled = True
c.content.blocking.method = "auto"

c.content.cookies.accept = "no-3rdparty"
c.content.autoplay = False  # Don't autoplay videos
c.content.headers.do_not_track = True
c.content.canvas_reading = False
