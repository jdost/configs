if has_key(g:plugs, 'nvim-lspconfig')
  lua << EOF
  local lspconfig = require('lspconfig')
  local servers = {'denols', 'tsserver', 'eslint'}

  for _, server in ipairs(servers) do
    lspconfig[server].setup {
      on_attach = function(client, bufnr)
        vim.api.nvim_exec([[
          augroup lsp_document_highlight
            autocmd! * <buffer>
            "autocmd CursorHorld <buffer> lua vim.lsp.buf.hover()
          augroup END
          set updatetime=4000
        ]], false)
      end,
    }
  end
EOF
endif
