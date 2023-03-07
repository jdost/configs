local modes = require "modes"
local select = require "select"

-- Set hint characters to home row keys
select.label_maker = function ()
    local chars = charset("asdfjkl;")
    return trim(sort(reverse(chars)))
end
-- Additional bindings
modes.add_binds("normal", {
    { "<Control-n>", "Go to next tab.",
        function (w) w:next_tab() end
    },
    { "<Control-p>", "Go to previous tab.",
        function (w) w:prev_tab() end
    },
})
