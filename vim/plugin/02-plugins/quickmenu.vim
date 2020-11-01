if has_key(g:plugs, 'quickmenu.vim')
   let g:quickmenu_options = "HL"

   nnoremap <silent> <Leader><Leader> :call quickmenu#toggle(0)<CR>

   call g:quickmenu#current(0)
   call g:quickmenu#header("QuickMenu")
   call g:quickmenu#append('Git', 'call quickmenu#toggle(2)', 'Show git menu', '', 0, '')
   call g:quickmenu#append('Help', 'call quickmenu#toggle(10)', 'Show help menu', '', 0, '')
   call g:quickmenu#append('Reload config', 'so $MYVIMRC', 'Reload vimrc', '', 99, '')

   call g:quickmenu#current(2)
   call g:quickmenu#header("Git")

   call g:quickmenu#current(10)
   call g:quickmenu#header("Help")
endif

augroup quickmenu_settings
   autocmd FileType quickmenu setlocal foldmethod=marker
augroup END
