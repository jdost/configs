-- Touchpad settings
hl.config({
    input = {
        touchpad = {
            disable_while_typing = true,
        }
    }
})
-- Monitor settings
local builtinMonitor = "desc:Sharp Corporation 0x14F9"
local monitors = {
    {
        output = builtinMonitor,
        mode = "preferred",
        position = "0x0",
        scale = 1,
    }
}
for i, monitor in pairs(monitors) do
    hl.monitor(monitor)
end
-- Workspaces
setupWorkspaces(monitors, {
    { name = "term", persistent = true, layout = "scrolling" },
    { name = "web", persistent = true, layout = "monocle" },
    { name = "notes" },
    { name = "chat", layout = "monocle" },
    { name = "video", layout = "monocle" }
})
-- Mirror when docked
hl.monitor({
    output = "desc:ASUSTek COMPUTER INC PA278QV M4LMQS061475",
    mode = "preferred",
    position = "0x0",
    scale = 1,
    mirror = builtinMonitor
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
