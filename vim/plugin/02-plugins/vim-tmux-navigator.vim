" tmux-navigator
let g:tmux_navigator_no_mappings = 1
" Disable tmux navigator when zooming the Vim pane
let g:tmux_navigator_disable_when_zoomed = 1

if has_key(g:plugs, 'vim-tmux-navigator')
   nnoremap <silent> <C-J> :TmuxNavigateDown<cr>
   nnoremap <silent> <C-K> :TmuxNavigateUp<cr>
   nnoremap <silent> <C-H> :TmuxNavigateLeft<cr>
   nnoremap <silent> <C-L> :TmuxNavigateRight<cr>
   inoremap <silent> <C-J> <Esc>:TmuxNavigateDown<cr>
   inoremap <silent> <C-K> <Esc>:TmuxNavigateUp<cr>
   inoremap <silent> <C-H> <Esc>:TmuxNavigateLeft<cr>
   inoremap <silent> <C-L> <Esc>:TmuxNavigateRight<cr>
else  " Fall back to same behavior but just in vim
   nnoremap <silent> <C-J> <C-W><C-J>
   nnoremap <silent> <C-K> <C-W><C-K>
   nnoremap <silent> <C-H> <C-W><C-H>
   nnoremap <silent> <C-L> <C-W><C-L>
   inoremap <silent> <C-J> <Esc><C-W><C-J>
   inoremap <silent> <C-K> <Esc><C-W><C-K>
   inoremap <silent> <C-H> <Esc><C-W><C-H>
   inoremap <silent> <C-L> <Esc><C-W><C-L>
endif
