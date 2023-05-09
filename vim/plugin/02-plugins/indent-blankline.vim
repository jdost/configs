if has_key(g:plugs, 'indent-blankline.nvim')
  lua << EOF
require('indent_blankline').setup{
  filetype_exclude = {
    "TelescopeResults", "TelescopePrompt", "help", "terminal", "lspinfo",
    "alpha",
  },
  buftype_exclude = {"prompt", "terminal"},
  show_trailing_blankline_indent = false,
  show_first_indent_level = false,
  show_current_context = true,
  show_current_context_start = true,
}
EOF
endif
