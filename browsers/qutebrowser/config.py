config.load_autoconfig()
for module in config.configdir.glob("modules.d/*.py"):
    config.source(module)

# Core
c.backend = "webengine"

c.qt.args = [
    "enable-gpu-rasterization",
    "ignore-gpu-blocklist",
    "enable-features=AcceleratedVideoDecodeLinuxGL",
]

# Autosaving
c.auto_save.interval = 15000
c.auto_save.session = True

# Custom definitions
DEFAULT = "ddg"
searchengines = {
    "g": "https://google.com/search?hl=en&q={}",
    "ddg": "https://duckduckgo.com/?q={}",
    "arch": "https://wiki.archlinux.org/?search={}",
    "archpkg": "https://archlinux.org/packages/?q={}",
    "aur": "https://aur.archlinux.org/packages/?O=0&K={}",
    "apt": "https://packages.ubuntu.com/search?keywords={}&searchon=names",
    "steam": "https://store.steampowered.com/search?term={}",
    "protondb": "https://www.protondb.com/search?q={}",
}
c.url.searchengines = {
    "DEFAULT": searchengines[DEFAULT],
    **searchengines,
}

# External opening behavior
c.new_instance_open_target = "tab"
c.new_instance_open_target_window = "last-focused"

# Misc
c.changelog_after_upgrade = "major"
c.content.fullscreen.window = True
c.tabs.mousewheel_switching = False
c.tabs.select_on_remove = "last-used"
