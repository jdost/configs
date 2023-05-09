if has_key(g:plugs, 'nvim-lspconfig')
  if has_key(g:plugs, 'ncm2')
    lua << EOF
      local servers = {'pylsp', 'pyright'}
      local lspconfig = require('lspconfig')
      local ncm2 = require('ncm2')

      for _, server in ipairs(servers) do
        lspconfig[server].setup {
          on_init = ncm2.register_lsp_source
        }
      end
EOF
  else
    lua << EOF
      local servers = {'pylsp', 'pyright'}
      local lspconfig = require('lspconfig')

      for _, server in ipairs(servers) do
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

if has_key(g:plugs, 'ale')
  if !has_key(g:plugs, 'nvim-lspconfig')
    " Ale specific settings for python
    let b:ale_fixers = ['black', 'isort', 'autoimport']
    let b:ale_linters = ['vim-lsp', 'mypy']
  else
    let b:ale_fixers = ['autoimport', 'isort']
    let b:ale_linters = []

    let b:ale_python_isort_options = "--settings-path ~/.config/isort.cfg"
  endif
endif
