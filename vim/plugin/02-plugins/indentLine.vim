let g:indentLine_char = '│'

if has_key(g:plugs, 'indentLine')
  " keymapping
  nnoremap <leader>ig <Plug>IndentLinesToggle

  if has_key(g:plugs, 'quickmenu.vim')
    call g:quickmenu#current(0)
    call g:quickmenu#append('Toggle indent lines', 'IndentLinesToggle', 'Toggle indent lines', '', 1, '')
  endif
endif
