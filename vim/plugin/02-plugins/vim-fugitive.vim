function! HelpVim_fugitive()
   echo ':Gblame           Opens the blame list for each line on the left'
   echo ':Glog             Opens a navigatable log for commits on the current file'
endfunction

if has_key(g:plugs, 'vim-fugitive')
   if has_key(g:plugs, 'quickmenu.vim')
      call g:quickmenu#current(2)
      call g:quickmenu#append('Blame', 'Gblame', 'git blame', '', 0, '')
      call g:quickmenu#append('Logs', 'Glog', 'git log', '', 0, '')

      call g:quickmenu#current(10)
      call g:quickmenu#append('Fugitive', 'call HelpVim_fugitive()', '', '', 0, '')
   endif

   if has_key(g:plugs, 'lightline.vim')
      let g:lightline.component.fugitive = '%{exists("*fugitive#head")?fugitive#head():""}'
      let g:lightline.component_visible_condition.fugitive = '(exists("*fugitive#head") && ""!=fugitive#head())'
   endif
endif
