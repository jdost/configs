if has_key(g:plugs, 'codewindow.nvim')
  lua << EOF
local codewindow = require('codewindow')
codewindow.setup{
  active_in_terminals = true,
  auto_enable = true,
  exclude_filetypes = {"gitcommit", "help"}
}
codewindow.apply_default_keybinds()
EOF
endif
