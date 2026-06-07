hl.config({
  debug = {
      disable_logs = false,
  }
})
-- Monitors
hl.monitor({
    output   = "",
    mode     = "preferred",
    position = "auto",
    scale    = "auto",
})
-- Launch the all the hooks
hl.on("hyprland.start", function ()
   hl.exec_cmd("~/.config/wayland/rc.sh")
end)
-- XDG Environment Variables
hl.env("XDG_CURRENT_DESKTOP", "Hyprland")
hl.env("XDG_SESSION_TYPE", "wayland")
hl.env("XDG_SESSION_DESKTOP", "Hyprland")
-- Input
hl.config({
    input = {
        kb_layout  = "us",
        kb_variant = "",
        kb_model   = "",
        kb_options = "",
        kb_rules   = "",

        follow_mouse = 2,
        mouse_refocus = false,
        float_switch_override_focus = 0,

        sensitivity = 0, -- -1.0 - 1.0, 0 means no modification.
    },
})
hl.config({
    cursor = {
        no_warps = true,
    },
})
-- General
hl.config({
    general = {
        gaps_in = 20,
        gaps_out = { top = 2, left = 40, right = 40, bottom = 40 },
        border_size = 8,

        col = {
            active_border = "rgba(33ccff75)",
            inactive_border = "rgba(59595955)",
        },
        -- Please see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Tearing/ before you turn this on
        allow_tearing = false,

        layout = "master",
    },
    decoration = {
        rounding = 6,
        -- Change transparency of focused and unfocused windows
        dim_inactive = true,
        dim_strength = 0.05,

        shadow = {
            enabled = false,
        },

        blur = {
            enabled = true,
            size = 5,
            passes = 2,
            vibrancy = 0.1696,
        },
    },
    animations = {
        enabled = true,
    },
})
-- Layouts
hl.config({
    dwindle = {
        preserve_split = true, -- You probably want this
    },
})
hl.config({
    master = {
        new_on_top = true,
    },
})
-- X11 Compatibility
hl.config({
    xwayland = {
        enabled = true,
        force_zero_scaling = true,
    },
})
hl.window_rule({
    name = "XWayland Border Identifier",
    match = { xwayland = true },
    border_color = "rgba(8866ff75)",
})
-- This is a weird one, webcord popups are actually un-classed floating windows and get blurred
hl.window_rule({
    name = "XWayland Webcord Popup fix",
    match = { xwayland = true, class = "", float = true},
    no_blur = true,
})
-- xwaylandbridge settings, source: https://wiki.hyprland.org/Useful-Utilities/Screen-Sharing/#xwayland
hl.window_rule({
    name = "XWaylandBridge Settings",
    match = { class = "xwaylandbridge" },
    no_initial_focus = true,
    no_focus = true,
    no_anim = true,
    no_blur = true,
    max_size = {1, 1},
    opacity = 0.0,
})
-- Misc
hl.config({
    misc = {
        disable_hyprland_logo = true,
        exit_window_retains_fullscreen = true,
        focus_on_activate = true,
        force_default_wallpaper = 0,
        mouse_move_focuses_monitor = false,
    },
})
hl.config({
    ecosystem = {
        no_donation_nag = true,
        no_update_news = true,
    },
})
-- Common Window/Layer rules
-- Blur the rofi overlay layer
hl.layer_rule({
    name = "rofi overlay",
    match = { namespace = "rofi" },
    blur = true,
})
-- Ignore maximize events
hl.window_rule({
    name  = "suppress-maximize-events",
    match = { class = ".*" },
    suppress_event = "maximize",
})
-- Dim inactive terminals, only thing that I really mix up
hl.window_rule({
    name  = "Dim inactive terminals",
    match = { class = "org.wezfurlog.wezterm" },
    opacity = "1.0 0.8 1.0",  -- <active> <inactive> <fullscreen>
})
-- Focus pinentry popups
hl.window_rule({
    name  = "Hold focus for pinentry popups",
    match = { class = "pinentry-*" },
    stay_focused = true,
})
-- Workspace Routing
hl.window_rule({
    name = "Firefox->Web",
    match = { class = "firefox" },
    workspace = "web",
})
hl.window_rule({
    name = "Qutebrowser->Web",
    match = { class = "org.qutebrower.qutebrower" },
    workspace = "web",
})
hl.window_rule({
    name = "Discord->chat",
    match = { class = "WebCord" },
    workspace = "chat",
})
hl.window_rule({
    name = "Obsidian->notes",
    match = { class = "obsidian" },
    workspace = "notes",
})
hl.window_rule({
    name = "PrismLauncher->games",
    match = { class = "org.prismlaunch.PrismLauncher" },
    workspace = "games",
})
-- Load additional configs
mainMod = "SUPER"
require("modules")

hl.bind(mainMod .. " + Q", hl.dsp.exit())
