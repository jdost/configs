if has_key(g:plugs, 'nvim-lspconfig')
  lua << EOF
  --local lspconfig = require('lspconfig')
  local servers = {'gopls'}

  for _, server in ipairs(servers) do
    vim.lsp.config(server, {
      on_attach = function(client, bufnr)
        vim.api.nvim_exec([[
          augroup lsp_document_highlight
            autocmd! * <buffer>
            "autocmd CursorHorld <buffer> lua vim.lsp.buf.hover()
          augroup END
          set updatetime=4000
        ]], false)
      end,
    })
  end
EOF
endif
