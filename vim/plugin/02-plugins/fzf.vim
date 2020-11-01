let s:current_state = 0

function! s:rotate_through(...)
   let s:current_state += 1
   if s:current_state == 0
      call fzf#vim#buffers()
   elseif s:current_state == 1
      call fzf#vim#gitfiles('')
   elseif s:current_state == 2
      call fzf#vim#history()
      let s:current_state = -1
   endif
endfunction

let g:fzf_action = {
   \ 'ctrl-f' : function('s:rotate_through'),
   \ }

function! s:start_fzf(...)
   let s:current_state = 0
   call fzf#vim#buffers()
endfunction


silent! if has_key(g:plugs, 'fzf.vim')
   nnoremap <C-P> :Files<cr>
endif
