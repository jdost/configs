if has_key(g:plugs, 'quickmenu.vim') && has_key(g:plugs, 'vim-obsession')
   call g:quickmenu#current(0)
   call g:quickmenu#append('Obsession', 'Obession', '', '', 0, '')
endif
