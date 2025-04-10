if !empty(glob($HOME.'/.local/python-code-tools'))
  let $PATH .= ':'.$HOME.'/.local/python-code-tools/bin'
endif

if has_key(g:plugs, 'nvim-lint')
  lua << EOF
    local lint = require('lint')
    lint.linters_by_ft['python'] = {'mypy', 'ruff'}
EOF
endif

if has_key(g:plugs, 'conform.nvim')
  lua << EOF
    local conform = require('conform')
    conform.formatters_by_ft.python = {
      'ruff_fix', 'ruff_organize_imports', 'ruff_format'
    }
EOF
endif

if has_key(g:plugs, 'nvim-lspconfig')
  if has_key(g:plugs, 'ncm2')
    lua << EOF
      local servers = {'pylsp', 'pyright'}
      local lspconfig = require('lspconfig')
      local ncm2 = require('ncm2')

      for _, server in ipairs(servers) do
        if vim.fn.executable(server) == 1 and lspconfig[server] == nil then
          lspconfig[server].setup {
            on_init = ncm2.register_lsp_source
          }
        end
      end
EOF
  else
    lua << EOF
      local servers = {'pylsp', 'pyright'}
      local lspconfig = require('lspconfig')

      for _, server in ipairs(servers) do
        if vim.fn.executable(server) == 1 then
          lspconfig[server].setup {
            on_attach = function(client, bufnr)
              vim.api.nvim_exec([[
                augroup lsp_document_highlight
                  autocmd! * <buffer>
                  "autocmd CursorHold <buffer> lua vim.lsp.buf.hover()
                  autocmd CursorHold <buffer> Lspsaga hover_doc
                augroup END
                set updatetime=1000
              ]], false)
            end,
          }
        end
      end
EOF
  endif
elseif has_key(g:plugs, 'vim-lsp')
  augroup asyncomplete_lsp_python
    autocmd!
    " pip install python-language-server
    au User lsp_setup call lsp#register_server({
      \ 'name': 'pylsp',
      \ 'cmd': {server_info->['pylsp']},
      \ 'whitelist': ['python'],
      \ })
  augroup END
endif
