if has_key(g:plugs, 'conform.nvim')
  lua << EOF
    local conform = require('conform')

    conform.setup({
      formatters_by_ft = { },
      format_on_save = {
        timeout_ms = 200,
        lsp_format = "fallback",
      },
    })
EOF
endif
