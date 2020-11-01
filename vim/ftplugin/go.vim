if executable('gopls') && has_key(g:plugs, 'vim-lsp')
   augroup asyncomplete_lsp_golang
      autocmd!
      " go get -u golang.org/x/tools/cmd/gopls
      au User lsp_setup call lsp#register_server({
         \ 'name': 'gopls',
         \ 'cmd': {server_info->['gopls', '-mode', 'stdio']},
         \ 'whitelist': ['go'],
         \ })
      autocmd BufWritePre *.go LspDocumentFormatSync
   augroup END
elseif executable('go-langserver') && has_key(g:plugs, 'vim-lsp')
   augroup asyncomplete_lsp_golang
      autocmd!
      " go get -u github.com/sourcegraph/go-langserver
      au User lsp_setup call lsp#register_server({
         \ 'name': 'go-langserver',
         \ 'cmd': {server_info->['go-langserver', '-gocodecompletion']},
         \ 'whitelist': ['go'],
         \ })
      autocmd BufWritePre *.go LspDocumentFormatSync
   augroup END
elseif executable('bingo') && has_key(g:plugs, 'vim-lsp')
   augroup asyncomplete_lsp_golang
      autocmd!
      " go get -u github.com/saibing/bingo
      au User lsp_setup call lsp#register_server({
         \ 'name': 'bingo',
         \ 'cmd': {server_info->['bingo', '-mode', 'stdio']},
         \ 'whitelist': ['go'],
         \ })
   augroup END
endif
