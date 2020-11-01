" Overall disable
let g:mundo_disable = 0

if has_key(g:plugs, 'vim-mundo')
   nnoremap <F5> :MundoToggle<CR>
endif

if has_key(g:plugs, 'quickmenu.vim') && has_key(g:plugs, 'vim-mundo')
   call g:quickmenu#current(0)
   call g:quickmenu#append('Open Undo-Tree', 'MundoToggle', 'Show undo-tree', '', 0, '')
endif
