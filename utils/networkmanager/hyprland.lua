-- nmtui launching should be a float since it *should* just be shortlived connecting
hl.window_rule({
    name = "NetworkManager TUI",
    match = { class = "nmtui" },

    float = true,
    center = true,
    size = { 600, 500 },
})
