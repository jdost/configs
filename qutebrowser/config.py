config.load_autoconfig()

# Core
c.backend = "webengine"
c.editor.command = ["alacritty", "--command", "vim -f {file} -c normal {line}G{column0}"]

# Hints
c.hints.mode = "letter"  # use the `chars` values
c.hints.chars = "asdfjkl;"
c.hints.auto_follow = "unique-match"
c.hints.hide_unmatched_rapid_hints = True

c.hints.border = "1px solid #282A36"
c.hints.padding = {
    "top": 1, "bottom": 1,
    "left": 2, "right": 2,
}

# Autosaving
c.auto_save.interval = 15000
c.auto_save.session = True

# Colortheme/Look (based on Dracula)
c.scrolling.bar = "when-searching"
c.colors.webpage.darkmode.enabled = True

c.colors.completion.category.bg = "#282A36"
c.colors.completion.category.border.bottom = "#282A36"
c.colors.completion.category.border.top = "#282A36"
c.colors.completion.category.fg = "#F8F8F2"
c.colors.completion.even.bg = "#282A36"
c.colors.completion.odd.bg = "#282A36"
c.colors.completion.fg = "#F8F8F2"
c.colors.completion.item.selected.bg = "#44475A"
c.colors.completion.item.selected.border.bottom = "#44475A"
c.colors.completion.item.selected.border.top = "#44475A"
c.colors.completion.item.selected.fg = "#F8F8F2"
c.colors.completion.match.fg = "#FFB86C"
c.colors.completion.scrollbar.bg = "#282A36"
c.colors.completion.scrollbar.fg = "#F8F8F2"

c.colors.downloads.bar.bg = "#282A36"
c.colors.downloads.error.bg = "#282A36"
c.colors.downloads.error.fg = "#FF5555"
c.colors.downloads.stop.bg = "#282A36"

c.colors.hints.bg = "#282A36"
c.colors.hints.fg = "#BD93F9"
c.colors.hints.match.fg = "#E0E0E0"

c.colors.keyhint.bg = "#282A36"
c.colors.keyhint.fg = "#BD93F9"
c.colors.keyhint.suffix.fg = "#44475A"

c.colors.messages.error.bg = "#282A36"
c.colors.messages.error.border = "#282A36"
c.colors.messages.error.fg = "#FF5555"
c.colors.messages.info.bg = "#282A36"
c.colors.messages.info.border = "#282A36"
c.colors.messages.info.fg = "#6272A4"
c.colors.messages.warning.bg = "#282A36"
c.colors.messages.warning.border = "#282A36"
c.colors.messages.warning.fg = "#FF5555"

c.colors.prompts.bg = "#282A36"
c.colors.prompts.border = "1px solid #282A36"
c.colors.prompts.fg = "#8BE9FD"
c.colors.prompts.selected.bg = "#44475A"

c.colors.statusbar.caret.bg = "#282A36"
c.colors.statusbar.caret.fg = "#FFB86C"
c.colors.statusbar.caret.selection.bg = "#282A36"
c.colors.statusbar.caret.selection.fg = "#FFB86C"
c.colors.statusbar.command.bg = "#282A36"
c.colors.statusbar.command.fg = "#FF79C6"
c.colors.statusbar.command.private.bg = "#282A36"
c.colors.statusbar.command.private.fg = "#E0E0E0"
c.colors.statusbar.insert.bg = "#181920"
c.colors.statusbar.insert.fg = "#FFFFFF"
c.colors.statusbar.normal.bg = "#282A36"
c.colors.statusbar.normal.fg = "#F8F8F2"
c.colors.statusbar.passthrough.bg = "#282A36"
c.colors.statusbar.passthrough.fg = "#FFB86C"
c.colors.statusbar.private.bg = "#282A36"
c.colors.statusbar.private.fg = "#E0E0E0"
c.colors.statusbar.progress.bg = "#282A36"
c.colors.statusbar.url.error.fg = "#FF5555"
c.colors.statusbar.url.fg = "#F8F8F2"
c.colors.statusbar.url.hover.fg = "#8BE9FD"
c.colors.statusbar.url.success.http.fg = "#50FA7B"
c.colors.statusbar.url.success.https.fg = "#50FA7B"
c.colors.statusbar.url.warn.fg = "#F1FA8C"

c.colors.tabs.bar.bg = "#44475A"
c.colors.tabs.even.bg = "#44475A"
c.colors.tabs.even.fg = "#F8F8F2"
c.colors.tabs.indicator.error = "#FF5555"
c.colors.tabs.indicator.start = "#FFB86C"
c.colors.tabs.indicator.stop = "#50FA7B"
c.colors.tabs.odd.bg = "#44475A"
c.colors.tabs.odd.fg = "#F8F8F2"
c.colors.tabs.selected.even.bg = "#282A36"
c.colors.tabs.selected.even.fg = "#F8F8F2"
c.colors.tabs.selected.odd.bg = "#282A36"
c.colors.tabs.selected.odd.fg = "#F8F8F2"


# Adblocking/Privacy
c.content.blocking.adblock.lists = [
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
    "https://easylist.to/easylist/fanboy-social.txt",
    "https://secure.fanboy.co.nz/fanboy-annoyance.txt",
]
c.content.blocking.enabled = True
c.content.blocking.method = "auto"

c.content.cookies.accept = "no-3rdparty"
c.content.autoplay = False  # Don'ta autoplay videos
c.content.headers.do_not_track = True

# Misc
c.changelog_after_upgrade = "major"
c.content.fullscreen.window = True
