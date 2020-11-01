if has_key(g:plugs, 'vim-rhubarb')
   if has_key(g:plugs, 'quickmenu.vim')
      call g:quickmenu#current(2)
      call g:quickmenu#append('Open', 'GitBrowse', 'Open this line in its web UI', '', 0, '')
   endif
endif
