if executable('rls')
  if has_key(g:plugs, 'vim-lsp')
    augroup asyncomplete_lsp_rust
      autocmd!
      " rustup component add rls rust-analysis rust-src
      au User lsp_setup call lsp#register_server({
        \ 'name': 'rls',
        \ 'cmd': {server_info->['rustup', 'run', 'stable', 'rls']},
        \ 'workspace_config': {'rust': {'clippy_preference': 'on'}},
        \ 'whitelist': ['rust'],
        \ })

      let g:ale_linters.rust = ['vim-lsp']
    augroup END
  elseif has_key(g:plugs, 'nvim-lspconfig') && has_key(g:plugs, 'ncm2')
    lua << EOF
local ncm2 = require('ncm2')
require'lspconfig'.rls.setup{on_init = ncm2.register_lsp_source}
EOF
  elseif has_key(g:plugs, 'nvim-lspconfig')
    lua << EOF
require'lspconfig'.rls.setup{}
EOF
  endif
elseif executable('rust-analyzer')
  if has_key(g:plugs, 'nvim-lspconfig') && has_key(g:plugs, 'ncm2')
    lua << EOF
local ncm2 = require('ncm2')
require'lspconfig'.rust_analyzer.setup{on_init = ncm2.register_lsp_source}
EOF
  elseif has_key(g:plugs, 'nvim-lspconfig')
    lua << EOF
require'lspconfig'.rust_analyzer.setup{}
EOF
  endif
endif
