hl.config({
    animations = { enabled = true }
})
-- Curves
hl.curve("overshot", { type = "bezier", points = { {0.05, 0.9}, {0.1, 1.05}}})
hl.curve("smoothOut", { type = "bezier", points = { {0.5, 0}, {0.99, 0.99}}})
-- Animations settings
hl.animation({ leaf = "windows", enabled = true, speed = 6, bezier = "overshot", style = "slide" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 5, bezier = "overshot", style = "slideFade" })
hl.animation({ leaf = "fadeSwitch", enabled = true, speed = 2.5, bezier = "smoothOut" })
hl.animation({ leaf = "fadeDim", enabled = true, speed = 2.5, bezier = "smoothOut" })
hl.animation({ leaf = "fadeDpms", enabled = true, speed = 1.5, bezier = "smoothOut" })
-- Disables
hl.animation({ leaf = "layers", enabled = false })
hl.animation({ leaf = "fade", enabled = false })
hl.animation({ leaf = "border", enabled = false })
hl.animation({ leaf = "borderangle", enabled = false })
hl.animation({ leaf = "specialWorkspace", enabled = false })
-- Exceptions
hl.window_rule({  -- Animations are weird with the fake fullscreen hyprland uses
    name = "Disable Animations: Fullscreen",
    match = { fullscreen = true },
    no_anim = true,
})
hl.window_rule({   -- Some floating windows are weird, so just disable for all
    name = "Disable Animations: Floating",
    match = { float = true },
    no_anim = true,
})
