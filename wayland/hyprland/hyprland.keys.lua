-- General
hl.bind(
    mainMod .. " + Return",
    hl.dsp.exec_cmd("systemd-run --user --slice=shell.slice wezterm start --always-new-process"),
    { description = "Launch Terminal" }
)
hl.bind(
    mainMod .. " + SHIFT + Q",
    hl.dsp.exit(),
    { description = "Close WM" }
)
hl.bind(
    mainMod .. " + SHIFT + C",
    hl.dsp.window.close(),
    { description = "Close window" }
)
hl.bind(
    mainMod .. " + Space",
    hl.dsp.window.fullscreen({ mode = "maximized", action = "toggle" }),
    { description = "Toggle window fullscreen" }
)
hl.bind(
    mainMod .. " + P",
    hl.dsp.exec_cmd("rofi -show combi"),
    { description = "Open Rofi application launcher" }
)
hl.bind(
    mainMod .. " + SHIFT + P",
    hl.dsp.exec_cmd("rofi -theme auth -show combi"),
    { description = "Open Rofi auth helper" }
)
hl.bind(
    mainMod .. " + SHIFT + F10",
    hl.dsp.exec_cmd("rofi-screencap select"),
    { description = "Launch screenshot helper in select mode" }
)
hl.bind(
    mainMod .. " + SHIFT + Print",
    hl.dsp.exec_cmd("rofi-screencap select"),
    { description = "Launch screenshot helper in select mode" }
)
-- Floating
hl.bind(
    mainMod .. " + F",
    hl.dsp.window.float({ action = "toggle" }),
    { description = "Toggle window between floating" }
)
hl.bind(
    mainMod .. " + mouse:272",
    hl.dsp.window.drag(),
    { description = "Move floating window", mouse = true }
)
hl.bind(
    mainMod .. " + mouse:273",
    hl.dsp.window.resize(),
    { description = "Resize floating window", mouse = true }
)
-- Focus change
hl.bind(
    mainMod .. " + Tab",
    function ()
        local workspace = hl.get_active_workspace()
        if workspace.tiled_layout == "monocle" then
            hl.dispatch(hl.dsp.layout("cyclenext"))
        else
            hl.dispatch(hl.dsp.window.cycle_next())
        end
    end,
    { description = "Cycle to next window" }
)
hl.bind(
    mainMod .. " + SHIFT + Tab",
    function ()
        local workspace = hl.get_active_workspace()
        if workspace.tiled_layout == "monocle" then
            hl.dispatch(hl.dsp.layout("cycleprev"))
        else
            hl.dispatch(hl.dsp.window.cycle_next({ next = false }))
        end
    end,
    { description = "Cycle to previous window" }
)
-- Directional Bindings
local keys =       { "L",      "H",      "K",      "J" }
local directions = { "right",  "left",   "up",     "down" }
local resizeDims = { { 10, 0}, {-10, 0}, {0, -10}, {0, 10} }
for i = 1, 4 do
    local key = keys[i]
    local direction = directions[i]
    -- Focus Shifting
    hl.bind(
        mainMod .. " + " .. key,
        hl.dsp.focus({ direction = direction }),
        { description = "Focus " .. direction }
    )
    -- Window Shift
    hl.bind(
        mainMod .. " + SHIFT + " .. key,
        hl.dsp.window.swap({ direction = direction }),
        { description = "Swap window " .. direction }
    )
    -- Anchor Shifting
    hl.bind(
        mainMod .. " + CTRL + " .. key,
        hl.dsp.window.move({ direction = direction }),
        { description = "Move window " .. direction }
    )
    -- Split Sizing
    local descriptionOp = ((resizeDims[i][1] + resizeDims[i][2]) > 0) and "Expand" or "Shrink"
    local descriptionDir = (resizeDims[i][1] == 0) and "vertically" or "horizontally"
    hl.bind(
        mainMod .. " + ALT + " .. key,
        hl.dsp.window.resize({ x = resizeDims[i][1], y = resizeDims[i][2], relative = true }),
        { description = descriptionOp .. " window " .. descriptionDir, repeating = true }
    )
end
-- Workspaces shifting
for i = 1, workspaceCount do
    hl.bind(
        mainMod .. " + " .. (i % 10),
        function ()
            local calculatedId = hl.get_active_monitor().id * workspaceCount + i
            hl.dispatch(hl.dsp.focus({ workspace = calculatedId }))
        end,
        { description = "Switch to workspace " .. i }
    )
    hl.bind(
        mainMod .. " + SHIFT + " .. (i % 10),
        function ()
            local calculatedId = hl.get_active_monitor().id * workspaceCount + i
            hl.dispatch(hl.dsp.window.move({ workspace = calculatedId }))
        end,
        { description = "Window: Send to workspace " .. i }
    )
end
-- Layout:Master
hl.bind(
    mainMod .. " + Equal",
    hl.dsp.layout("addmaster"),
    { description = "Add window to primary pane" }
)
hl.bind(
    mainMod .. " + Minus",
    hl.dsp.layout("removemaster"),
    { description = "Remove window from primary pane" }
)
-- Media/Special keys
local volumeKeys = {
    { "XF86AudioRaiseVolume", "+"},
    { "XF86AudioLowerVolume" , "-"}
}
for i = 1, 2 do
    local key = volumeKeys[i][1]
    local dir = volumeKeys[i][2]
    hl.bind(
        key,
        hl.dsp.exec_cmd("pulsemixer --change-volume " .. dir .. "10"),
        { locked = true, repeating = true }
    )
    hl.bind(
        "SHIFT + " .. key,
        hl.dsp.exec_cmd("pulsemixer --change-volume " .. dir .. "1"),
        { locked = true, repeating = true }
    )
    hl.bind(
        "CTRL + " .. key,
        hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SOURCE@ 10%" .. dir),
        { locked = true, repeating = true }
    )
end
hl.bind(
    "XF86AudioMute", hl.dsp.exec_cmd("pulsemixer --toggle-mute")
)
hl.bind(
    "CTRL + XF86AudioMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle")
)
-- Brightness, really only on laptops
hl.bind(
    "XF86MonBrightnessDown",
    hl.dsp.exec_cmd("brightnessctl s -- '-5%'"),
    { locked = true, repeating = true }
)
hl.bind(
    "XF86MonBrightnessUp",
    hl.dsp.exec_cmd("brightnessctl s -- '+5%'"),
    { locked = true, repeating = true }
)
-- Media
hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl --current play-pause"))
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl --current previous"))
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl --current next"))
