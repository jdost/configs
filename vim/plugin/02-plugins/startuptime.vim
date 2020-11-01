if has_key(g:plugs, 'quickmenu.vim') && has_key(g:plugs, 'startuptime.vim')
   call g:quickmenu#current(0)
   call g:quickmenu#append('Analyze Startuptime', 'StartupTime', '', 1, '')
endif
