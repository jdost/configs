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

if has_key(g:plugs, 'indentLine')
  " The indentLine plugin messes with the conceal plugin for python
  let b:indentLine_enabled = 0
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
