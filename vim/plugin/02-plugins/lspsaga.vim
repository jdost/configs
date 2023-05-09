if has_key(g:plugs, 'lspsaga.nvim')
  lua << EOF
    local saga = require('lspsaga')

    saga.setup({
      lightbulb = {
        enable = false,
      }
    })
EOF
endif
