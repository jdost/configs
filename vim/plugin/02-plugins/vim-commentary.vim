if has_key(g:plugs, 'vim-commentary')
   xmap <Leader>c <Plug>Commentary
   nmap <Leader>c <Plug>Commentary
   omap <Leader>c <Plug>Commentary

   nmap <Leader>cc <Plug>CommentaryLine
   nmap <Leader>cu <Plug>Commentary<Plug>Commentary
endif
