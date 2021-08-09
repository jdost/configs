setlocal tabstop=4
setlocal shiftwidth=4

setlocal wrap
setlocal textwidth=79
setlocal colorcolumn=80

setlocal foldmethod=indent

if !empty(glob($HOME . '/.local/python-code-tools'))
  let $PATH=$HOME . '/.local/python-code-tools/bin:' . $PATH
endif

if executable('pyls') && has_key(g:plugs, 'vim-lsp')
  augroup asyncomplete_lsp_python
    autocmd!
    " pip install python-language-server
    au User lsp_setup call lsp#register_server({
      \ 'name': 'pyls',
      \ 'cmd': {server_info->['pyls']},
      \ 'whitelist': ['python'],
      \ })
  augroup END
endif

if executable('pylsp') && has_key(g:plugs, 'nvim-lspconfig')
  lua << EOF
local ncm2 = require('ncm2')
require'lspconfig'.pylsp.setup{on_init = ncm2.register_lsp_source}
EOF
endif

if has_key(g:plugs, 'ale')
  " Ale specific settings for python
  let b:ale_fixers = ['black', 'isort', 'autoimport']
  let b:ale_linters = ['vim-lsp', 'mypy']
  let b:ale_python_black_options = "--line-length 80"
endif

if has_key(g:plugs, 'indentLine')
  " The indentLine plugin messes with the conceal plugin for python
  let b:indentLine_enabled = 0
endif
