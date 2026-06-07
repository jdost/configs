-- NVidia settings
hl.env("LIBVA_DRIVER_NAME", "nvidia")
hl.env("GBM_BACKEND", "nvidia-drm")
hl.env("__GLX_VENDOR_LIBRARY_NAME", "nvidia")

hl.config({
    cursor = {
        no_hardware_cursors = true
    }
})
-- Monitors
local mainMonitor = "desc:ASUSTek COMPUTER INC PA278QV M4LMQS061475"
hl.monitor({
    output = mainMonitor,
    mode = "preferred",
    position = "0x0",
    scale = 1
})
local secondaryMonitor = "desc:Dell Inc. DELL U2415 CFV9N84T0N3U"
hl.monitor({
    output = secondaryMonitor,
    mode = "preferred",
    position = "2560x-400",
    scale = 1,
    transform = 3
})
-- Workspaces
hl.workspace_rule({ workspace = "1", default_name = "term", persistent = true, monitor = mainMonitor })
hl.workspace_rule({ workspace = "2", default_name = "web", persistent = true, monitor = mainMonitor })
hl.workspace_rule({ workspace = "3", default_name = "code", monitor = mainMonitor })
hl.workspace_rule({ workspace = "4", default_name = "games", monitor = mainMonitor })
hl.workspace_rule({ workspace = "5", default_name = "scratch", monitor = mainMonitor })
hl.workspace_rule({ workspace = "6", default_name = "notes", monitor = secondaryMonitor, gaps_out = 40, layout_opts = { orientation = "top" } })
hl.workspace_rule({ workspace = "7", default_name = "video", monitor = secondaryMonitor, gaps_out = 40, layout_opts = { orientation = "top" } })
hl.workspace_rule({ workspace = "8", default_name = "chat", monitor = secondaryMonitor, gaps_out = 40, layout_opts = { orientation = "top" } })
-- Prepopulate the persistent workspaces on launch
hl.on("hyprland.start", function ()
    hl.dispatch(hl.dsp.focus({ workspace = "1" }))
    hl.dispatch(hl.dsp.focus({ workspace = "2" }))
    hl.dispatch(hl.dsp.focus({ workspace = "1" }))
end)
-- Keys
hl.bind(
    mainMod .. " + e",
    hl.dsp.focus({ monitor = "l" }),
    { description = "Focus left monitor" }
)
hl.bind(
    mainMod .. " + r",
    hl.dsp.focus({ monitor = "r" }),
    { description = "Focus right monitor" }
)
hl.bind(
    mainMod .. " + SHIFT + e",
    hl.dsp.window.move({ monitor = "l" }),
    { description = "Move to left monitor" }
)
hl.bind(
    mainMod .. " + SHIFT + r",
    hl.dsp.window.move({ monitor = "r" }),
    { description = "Move to right monitor" }
)
-- Rules
hl.window_rule({
    name = "Scrcpy",
    match = { class = "scrcpy" },
    tile = true
})
hl.window_rule({
    name = "PrismLauncher->Games",
    match = { initial_class = "org.prismlauncher.PrismLauncher" },
    workspace = "4"
})
hl.window_rule({
    name = "Steam->Games",
    match = { initial_class = "steam" },
    workspace = "4"
})
hl.window_rule({
    name = "Obsidian->Chat",
    match = { class = "obsidian" },
    workspace = "6"
})
hl.window_rule({
    name = "Firefox->Video",
    match = { class = "firefox" },
    workspace = "7"
})
hl.window_rule({
    name = "mpv->Video",
    match = { class = "mpv" },
    workspace = "7"
})
hl.window_rule({
    name = "Webcord->Chat",
    match = { class = "WebCord" },
    workspace = "8"
})
hl.window_rule({
    name = "Webcord Fixes",
    match = { class = "WebCord" },
    no_blur = true
})
