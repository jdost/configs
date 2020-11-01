" Directory to store sessions
let g:prosession_dir = $XDG_CACHE_HOME. '/vim/session/'

if exists('$TMUX')
   " Let prosession set tmux pane name
   let g:prosession_tmux_title = 1
endif
" Whether to load/start a prosession on start
let g:prosession_on_startup = 1

function! HelpVim_prosession()
   echo ':Prosession {dir}             switch to the session of {dir}, if doesnt exist, creat a new session'
   echo ':ProsessionDelete [{dir}]     if no {dir} specified, delete current active session'
   echo ':ProsessionList {filter}      if no {filter} specified, list all session'
endfunction

if has_key(g:plugs, 'quickmenu.vim') && has_key(g:plugs, 'vim-prosession')
   call g:quickmenu#current(10)
   call g:quickmenu#append('Prosession', 'call HelpVim_prosession()', '', '', 0, '')
endif

if has_key(g:plugs, 'vim-prosession')
   command! -nargs=? ProsessionList echo prosession#ListSessions(<q-args>)

   augroup prosession_start
      autocmd!
   augroup END
endif
