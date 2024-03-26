if has_key(g:plugs, 'indent-blankline.nvim')
  lua << EOF
require('ibl').setup{
  exclude = {
    filetypes = {
      "TelescopeResults", "TelescopePrompt", "help", "terminal", "lspinfo",
      "alpha",
    },
    buftypes = {"prompt", "terminal"},
  },
  whitespace = {
    remove_blankline_trail = true,
  }
}

local hooks = require('ibl.hooks')
hooks.register(
  hooks.type.WHITESPACE,
  hooks.builtin.hide_first_tab_indent_level
)

hooks.register(
  hooks.type.WHITESPACE,
  hooks.builtin.hide_first_space_indent_level
)
EOF
endif
