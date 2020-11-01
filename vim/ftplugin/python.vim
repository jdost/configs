setlocal tabstop=4
setlocal shiftwidth=4

setlocal wrap
setlocal textwidth=79
setlocal colorcolumn=80

setlocal foldmethod=indent

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

if has_key(g:plugs, 'ale')
   " Ale specific settings for python
   let b:ale_fixers = ['black', 'isort']
endif
