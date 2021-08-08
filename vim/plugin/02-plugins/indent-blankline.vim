if has_key(g:plugs, 'indent-blankline.nvim')
  lua << EOF
require('indent_blankline').setup{
  filetype_exclude = {"TelescopeResults", "TelescopePrompt"},
  buftype_exclude = {"prompt"},
  show_trailing_blankline_indent = false,
  show_first_indent_level = false,
}
EOF
endif
