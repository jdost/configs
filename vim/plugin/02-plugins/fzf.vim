let s:current_state = 0

function! s:rotate_through(...)
  let s:current_state += 1
  echom 'rotation: ' . s:current_state
  if s:current_state == 0
    call fzf#vim#gitfiles('', fzf#vim#with_preview())
  elseif s:current_state == 1
    call fzf#vim#grep(
      \ "rg --column --line-number --no-heading --color=always --smart-case -- ".shellescape(''),
      \ 1, fzf#vim#with_preview())
  elseif s:current_state == 2
    let s:current_state = -1
    call fzf#vim#history('', fzf#vim#with_preview())
  endif
endfunction

let g:fzf_action_disabled = {
  \ 'ctrl-f' : function('s:rotate_through'),
  \ }

function! s:start_fzf(...)
  let s:current_state = 0
  call fzf#vim#buffers()
endfunction

silent! if has_key(g:plugs, 'fzf.vim')
  nnoremap <C-P> :GitFiles<cr>
endif
