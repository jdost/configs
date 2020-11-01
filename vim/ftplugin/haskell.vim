setlocal shiftwidth=2
setlocal tabstop=2

" disable the auto syntastic checking
silent! if has_key(g:plugs, 'syntastic')
   let g:syntastic_mode_map = { 'mode': 'passive',
      \  'active_filetypes': [],
      \  'passive_filetypes': ['haskell'] }
endif
