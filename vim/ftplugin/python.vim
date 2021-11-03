setlocal tabstop=4
setlocal shiftwidth=4

setlocal wrap
setlocal textwidth=79
setlocal colorcolumn=80

if has_key(g:plugs, 'nvim-treesitter')
  " Use treesitter for folding logic
  setlocal foldmethod=expr
  setlocal foldexpr=nvim_treesitter#foldexpr()
else
  setlocal foldmethod=indent
endif

if !empty(glob($HOME.'/.local/python-code-tools'))
  let $PATH .= ':'.$HOME.'/.local/python-code-tools/bin'
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

if executable('pyright')
  if has_key(g:plugs, 'nvim-lspconfig') && has_key(g:plugs, 'ncm2')
    lua << EOF
local ncm2 = require('ncm2')
require'lspconfig'.pyright.setup{on_init = ncm2.register_lsp_source}
EOF
    LspStart
  elseif has_key(g:plugs, 'nvim-lspconfig')
    lua << EOF
require'lspconfig'.pyright.setup{}
EOF
    LspStart
  endif
elseif executable('pylsp')
  if has_key(g:plugs, 'nvim-lspconfig') && has_key(g:plugs, 'ncm2')
    lua << EOF
local ncm2 = require('ncm2')
require'lspconfig'.pylsp.setup{on_init = ncm2.register_lsp_source}
EOF
    LspStart
  elseif has_key(g:plugs, 'nvim-lspconfig')
    lua << EOF
require'lspconfig'.pylsp.setup{}
EOF
    LspStart
  endif
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
