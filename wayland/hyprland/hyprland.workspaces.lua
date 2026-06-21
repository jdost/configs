workspaceCount = 10
-- Workspace Routing
local workspaceRoutes = {
    ["web"] = {
        ["Qutebrowser"] = "org.qutebrowser.qutebrowser"
    },
    ["chat"] = {
        ["Discord"] = "WebCord"
    },
    ["notes"] = {
        ["Obsidian"] = "obsidian"
    },
    ["games"] = {
        ["PrismLauncher"] = "org.prismlaunch.PrismLauncher",
        ["Steam"] = "steam"
    },
    ["video"] = {
        ["Firefox"] = "firefox",
        ["MPV"] = "mpv"
    }
}
-- Workspace setup
function setupWorkspaces(monitors, workspaces)
    local persisted = {}
    local monitorWorkspaces = {}
    for i, workspace in pairs(workspaces) do
        local targetMonitor = monitors[workspace.monitor or 1]
        if monitorWorkspaces[targetMonitor.output] == nil then
            monitorWorkspaces[targetMonitor.output] = 10 * ((workspace.monitor or 1) - 1) + 1
        end
        local id = monitorWorkspaces[targetMonitor.output]
        monitorWorkspaces[targetMonitor.output] = monitorWorkspaces[targetMonitor.output] + 1
        local layoutOpts = {}
        if ((targetMonitor.transform or 1) % 2 == 1) then
            layoutOpts = { orientation = "top" }
        end
        hl.workspace_rule({
            workspace = id,
            default_name = workspace.name,
            persistent = workspace.persistent,
            monitor = targetMonitor.output,
            layout = workspace.layout,
            layout_opts = layoutOpts
        })
        if (workspace.persistent) then
            table.insert(persisted, id)
        end
        if workspaceRoutes[workspace.name] then
            for name, class in pairs(workspaceRoutes[workspace.name]) do
                hl.window_rule({
                    name = name .. "->" .. workspace.name,
                    match = { class = class },
                    workspace = id
                })
            end
        end
    end

    hl.on("hyprland.start", function ()
        -- Pre-populate all peristent workspaces
        for i, workspace in pairs(persisted) do
            hl.dispatch(hl.dsp.focus({ workspace = workspace }))
        end
        -- Start with the first workspace open
        for i, monitor in pairs(monitors) do
            local id = (10 * (i-1) + 1)
            -- This isn't working for a second monitor, IDK why?
            hl.dispatch(hl.dsp.focus({ workspace = id }))
        end
        -- Always focus first monitor
        hl.dispatch(hl.dsp.focus({ workspace = "1" }))
    end)
end
