if has_key(g:plugs, 'git-messenger.vim')
   nnoremap <Leader>gm <Plug>(git-messenger)

   if has_key(g:plugs, 'quickmenu.vim')
      call g:quickmenu#current(2)
      call g:quickmenu#append('Git History', 'GitMessenger', 'Open last commit for this', '', 0, '')
   endif
endif
