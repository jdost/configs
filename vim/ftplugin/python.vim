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
require'lspconfig'.pylsp.setup{}
EOF
endif

if has_key(g:plugs, 'ale') && !has_key(g:plugs, 'nvim-lspconfig')
  " Ale specific settings for python
  let b:ale_fixers = ['black', 'isort', 'autoimport']
  let b:ale_linters = ['vim-lsp', 'mypy']
elseif has_key(g:plugs, 'ale')
  let b:ale_fixers = ['autoimport', 'isort']
  let b:ale_linters = []

  let b:ale_python_isort_options = "--settings-path ~/.config/isort.cfg"
endif

if has_key(g:plugs, 'indentLine')
  " The indentLine plugin messes with the conceal plugin for python
  let b:indentLine_enabled = 0
endif
