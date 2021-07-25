config.load_autoconfig()
for module in config.configdir.glob("modules.d/*.py"):
    config.source(module)

# Core
c.backend = "webengine"

# Autosaving
c.auto_save.interval = 15000
c.auto_save.session = True

# Custom definitions
c.url.searchengines = {
    "DEFAULT": "https://google.com/search?hl=en&q={}",
    "g": "https://google.com/search?hl=en&q={}",
    "ddg": "https://duckduckgo.com/?q={}",
    "arch": "https://wiki.archlinux.org/?search={}",
    "archpkg": "https://archlinux.org/packages/?q={}",
    "aur": "https://aur.archlinux.org/packages/?O=0&K={}",
}

# Misc
c.changelog_after_upgrade = "major"
c.content.fullscreen.window = True
c.tabs.mousewheel_switching = False
