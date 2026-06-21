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
local secondaryMonitor = "desc:Dell Inc. DELL U2415 CFV9N84T0N3U"
local monitors = {
    {
        output = mainMonitor,
        mode = "preferred",
        position = "0x0",
        scale = 1
    },
    {
        output = secondaryMonitor,
        mode = "preferred",
        position = "2560x-400",
        scale = 1,
        transform = 3
    }
}
for i, monitor in pairs(monitors) do
    hl.monitor(monitor)
end
-- Workspaces
setupWorkspaces(monitors, {
    { name = "term", persistent = true, layout = "scrolling" },
    { name = "web", persistent = true, layout = "monocle" },
    { name = "games" },
    -- Second monitor
    { name = "notes", monitor = 2 },
    { name = "video", monitor = 2 },
    { name = "chat", layout = "monocle", monitor = 2 }
})
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
    name = "Webcord Fixes",
    match = { class = "WebCord" },
    no_blur = true
})
