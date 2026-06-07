-- General rule
hl.window_rule({
    name = "Sidebars",
    match = { initial_class = "sidebar.*" },

    border_size = 2,
    float = true,
    no_anim = true,
    opacity = "1.0 0.4 1.0",
    rounding = 0,
    size = {"monitor_w * 0.33", "monitor_h - 4"}
})
-- Positioning
hl.window_rule({
    name = "Left Sidebar Position", match = { initial_class = "sidebar.left" },
    move = {"0", "2"}
})
hl.window_rule({
    name = "Right Sidebar Position", match = { initial_class = "sidebar.right" },
    move = {"monitor_w * 0.67 - 2", "2"}
})
-- Key bindings
local sides = {"right", "left"}
local sidebarCmd = "wezterm --config window_background_opacity=0.4 start --cwd $HOME"
for i = 1, 2 do
    local side = sides[i]
    hl.bind(
        mainMod .. " + Bracket" .. side,
        function ()
            local sidebarClass = "sidebar." .. side
            local window = hl.get_window("class:" .. sidebarClass)
            -- Spawn the window if it doesn't exist
            if window == nil then
                hl.dispatch(hl.dsp.exec_cmd(sidebarCmd .. " --class \"" .. sidebarClass .. "\""))
                return
            end
            -- If the active window, minimize/send to special workspace
            if window.active then
                hl.dispatch(hl.dsp.workspace.toggle_special("sidebars"))
                hl.dispatch(hl.dsp.window.move({workspace="special:sidebars", window=window}))
                hl.dispatch(hl.dsp.workspace.toggle_special("sidebars"))
                hl.dispatch(hl.dsp.window.cycle_next())
            -- If not active, but on workspace, focus
            elseif window.workspace.active then
                hl.dispatch(hl.dsp.focus({ window = window }))
            -- Otherwise, bring the window to the active workspace
            else
                hl.dispatch(hl.dsp.window.move({
                    workspace = hl.get_active_workspace(),
                    window = window
                }))
            end
        end,
        { description = "Toggle " .. side .. " Sidebar" }
    )
end
