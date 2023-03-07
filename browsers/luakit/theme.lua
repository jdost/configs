local theme = {}

-- Fonts
theme.font = "12px Hack Nerd Font Mono"
-- Colorscheme
theme.fg = "#22CCDD"
theme.bg = "#222222"

-- Hints
theme.hint_font = "10px Hack Nerd Font Mono"
theme.hint_fg = "#222222"
theme.hint_bg = "#CAAF2B"
theme.hint_border = "1px solid #222222"
theme.hint_opacity = "0.7"
theme.hint_overlay_bg = "rgba(255,255,153,0.7)"
theme.hint_overlay_border = "1px solid #000000"
theme.hint_overlay_selected_bg = "rgba(0,255,0,0.7)"
theme.hint_overlay_selected_border = theme.hint_overlay_border

-- General colour pairings
theme.ok = { fg = "#000", bg = "#FFF" }
theme.warn = { fg = "#F00", bg = "#FFF" }
theme.error = { fg = "#FFF", bg = "#F00" }
-- Genaral
theme.success_fg = "#0f0"
theme.loaded_fg  = "#33AADD"
-- Error
theme.error_fg = "#FFF"
theme.error_bg = "#F00"
-- Warning
theme.warning_fg = "#F00"
theme.warning_bg = "#FFF"
-- Notification
theme.notif_fg = "#444"
theme.notif_bg = "#FFF"
-- Menu
theme.menu_fg                   = "#000"
theme.menu_bg                   = "#fff"
theme.menu_selected_fg          = "#000"
theme.menu_selected_bg          = "#FF0"
theme.menu_title_bg             = "#fff"
theme.menu_primary_title_fg     = "#f00"
theme.menu_secondary_title_fg   = "#666"

theme.menu_disabled_fg = "#999"
theme.menu_disabled_bg = theme.menu_bg
theme.menu_enabled_fg = theme.menu_fg
theme.menu_enabled_bg = theme.menu_bg
theme.menu_active_fg = "#060"
theme.menu_active_bg = theme.menu_bg
-- Proxy manager
theme.proxy_active_menu_fg      = '#000'
theme.proxy_active_menu_bg      = '#FFF'
theme.proxy_inactive_menu_fg    = '#888'
theme.proxy_inactive_menu_bg    = '#FFF'
-- Statusbar
theme.sbar_fg         = "#fff"
theme.sbar_bg         = "#000"
-- Downloadbar
theme.dbar_fg         = "#fff"
theme.dbar_bg         = "#000"
theme.dbar_error_fg   = "#F00"
-- Input bar
theme.ibar_fg           = "#000"
theme.ibar_bg           = "rgba(0,0,0,0)"
-- Tabs
theme.tab_fg            = "#888"
theme.tab_bg            = "#222"
theme.tab_hover_bg      = "#292929"
theme.tab_ntheme        = "#ddd"
theme.selected_fg       = "#fff"
theme.selected_bg       = "#000"
theme.selected_ntheme   = "#ddd"
theme.loading_fg        = "#33AADD"
theme.loading_bg        = "#000"

theme.selected_private_tab_bg = "#3d295b"
theme.private_tab_bg    = "#22254a"
-- SSL Hinting
theme.trust_fg          = "#0F0"
theme.notrust_fg        = "#F00"
-- Gopher page style (override defaults)
theme.gopher_light = { bg = "#E8E8E8", fg = "#17181C", link = "#03678D" }
theme.gopher_dark  = { bg = "#17181C", fg = "#E8E8E8", link = "#f90" }

return theme
