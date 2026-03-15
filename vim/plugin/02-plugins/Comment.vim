if has_key(g:plugs, 'Comment.nvim')
  lua << EOF
    require('Comment').setup({
      toggler = {
        line = '<leader>cc',
      },
      opleader = {
        line = '<leader>c',
      },
    })
EOF
endif
