if has_key(g:plugs, 'gitsigns.nvim')
  lua << EOF
    require("gitsigns").setup({
    })
EOF
endif
