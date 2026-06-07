-- Monitor settings
local builtinMonitor = "desc:Sharp Corporation 0x14F9"
hl.monitor({
    output = builtinMonitor,
    mode = "preferred",
    position = "0x0",
    scale = 1,
})
-- Mirror when docked
local dockedMonitor = "desc:ASUSTek COMPUTER INC PA278QV M4LMQS061475"
hl.monitor({
    output = dockedMonitor,
    mode = "preferred",
    position = "0x0",
    scale = 1,
    mirror = builtinMonitor
})
-- Touchpad settings
hl.config({
    input = {
        touchpad = {
            disable_while_typing = true,
        }
    }
})
-- Special Keybindings
hl.bind(
    mainMod .. " + left",
    hl.dsp.focus({ workspace = "r-1" }),
    { description = "Move to previous workspace" }
)
hl.bind(
    mainMod .. " + right",
    hl.dsp.focus({ workspace = "r+1" }),
    { description = "Move to next workspace" }
)
-- Workspaces
hl.workspace_rule({ workspace = "1", default_name = "term", persistent = true, monitor = builtinMonitor })
hl.workspace_rule({ workspace = "2", default_name = "web", persistent = true, monitor = builtinMonitor })
hl.workspace_rule({ workspace = "3", default_name = "notes", monitor = builtinMonitor })
hl.workspace_rule({ workspace = "4", default_name = "chat", monitor = builtinMonitor })
hl.workspace_rule({ workspace = "5", default_name = "video", monitor = builtinMonitor })
-- Prepopulate the persistent workspaces on launch
hl.on("hyprland.start", function ()
    hl.dispatch(hl.dsp.focus({ workspace = "1" }))
    hl.dispatch(hl.dsp.focus({ workspace = "2" }))
    hl.dispatch(hl.dsp.focus({ workspace = "1" }))
end)
-- Rules for workspaces
hl.window_rule({
    name = "Qutebrowser->Web",
    match = { class = "org.qutebrowser.qutebrowser" },
    workspace = "2",
})
hl.window_rule({
    name = "Obsidian->Notes",
    match = { class = "obsidian" },
    workspace = "3",
})
hl.window_rule({
    name = "WebCord->Chat",
    match = { class = "WebCord" },
    workspace = "4",
})
hl.window_rule({
    name = "mpv->Video",
    match = { class = "mpv" },
    workspace = "5",
})
