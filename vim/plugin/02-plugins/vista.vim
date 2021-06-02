silent! if has_key(g:plugs, 'vista.vim')
  if has_key(g:plugs, 'vim-lsp')
    let g:vista_default_executive = 'vim_lsp'
  endif

  if has_key(g:plugs, 'quickmenu.vim')
    call g:quickmenu#current(0)
    call g:quickmenu#append('Toggle tags', 'Vista', 'Toggle tags', '', 1, '')
  endif
endif
