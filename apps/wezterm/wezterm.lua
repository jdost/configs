local wezterm = require 'wezterm';

colors = {
    foreground = "#22CCDD",
    background = "#000000",

    cursor_fg = "#000000",
    cursor_bg = "#22CCDD",

    selection_fg = "#000000",
    selection_bg = "#22CCDD",

    scrollbar_thumb = "#222222",
    split = "#444444",

    ansi = {
        "#222222", "#E01B1B", "#1BE01B", "#CAAF2B",
        "#4C8EA1", "#956D9D", "#7C9AA6", "#A3A3A3"
    },
    brights = {
        "#444444", "#CC896D", "#7DB37D", "#BFB556",
        "#6BC1D0", "#C18FCB", "#8FADBF", "#FFFFFF"
    },
}

return {
    bold_brightens_ansi_colors = true,
    check_for_updates = false,
    colors = colors,
    enable_tab_bar = false,
    exit_behavior = "Close",
    font = wezterm.font("Iosevka Term", {bold=false}),
    font_size = 11.0,
    keys = {
        {key="x", mods="CTRL", action=wezterm.action{CopyTo="Clipboard"}},
        {key="x", mods="CTRL|SHIFT", action=wezterm.action{CopyTo="PrimarySelection"}},
        {key="v", mods="CTRL", action=wezterm.action{PasteFrom="Clipboard"}},
        {key="v", mods="CTRL|SHIFT", action=wezterm.action{PasteFrom="PrimarySelection"}},
        {key="=", mods="CTRL", action = wezterm.action.IncreaseFontSize},
        {key="-", mods="CTRL", action = wezterm.action.DecreaseFontSize},
    },
    window_background_opacity = 0.65,
}
