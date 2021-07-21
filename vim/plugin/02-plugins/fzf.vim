let s:current_state = 0

function! s:rotate_through(...)
  let s:current_state += 1
  if s:current_state == 0
    call fzf#vim#gitfiles('', fzf#vim#with_preview())
  elseif s:current_state == 1
    call fzf#vim#history(fzf#vim#with_preview())
  elseif s:current_state == 2
    let s:current_state = -1
    call fzf#vim#files('', fzf#vim#with_preview())
  endif
endfunction

function! s:fzf_grep(...)
    call fzf#vim#grep(
      \ "rg --column --line-number --no-heading --color=always --smart-case -- ".shellescape(''),
      \ 1, fzf#vim#with_preview())
endfunction

function! s:fzf_buffers(...)
    call fzf#vim#buffers('', fzf#vim#with_preview())
endfunction

function! s:FZFstart(...)
  let s:current_state = 0
  call fzf#vim#gitfiles('', fzf#vim#with_preview())
endfunction

let g:fzf_action = {
  \ 'ctrl-f' : function('s:rotate_through'),
  \ 'ctrl-p' : function('s:fzf_buffers'),
  \ 'ctrl-l' : function('s:fzf_grep'),
  \ }

let g:fzf_layout = { 'down': '40%' }

augroup fzf
  autocmd!
  autocmd! FileType fzf
  autocmd  FileType fzf set laststatus=0 noshowmode noruler
    \| autocmd BufLeave <buffer> set laststatus=2 showmode ruler
augroup END

silent! if has_key(g:plugs, 'fzf.vim')
  "nnoremap <silent> <C-P> :GFiles<cr>
  nnoremap <silent> <C-P> :call <SID>FZFstart()<cr>
endif
