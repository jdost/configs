setlocal tabstop=2
setlocal shiftwidth=2

if executable('solargraph') && has_key(g:plugs, 'vim-lsp')
   augroup asyncomplete_lsp_ruby
      autocmd!
      " gem install solargraph
      au User lsp_setup call lsp#register_server({
         \ 'name': 'solargraph',
         \ 'cmd': {server_info->[&shell, &shellcmdflag, 'solargraph stdio']},
         \ 'initialization_options': {"diagnostics": "true"},
         \ 'whitelist': ['ruby'],
         \ })
   augroup END
endif
