function! LoadLocalVimrc()
  if !empty(glob('.local.vim'))
    source .local.vim
  endif
endfunction

if has_key(g:plugs, 'vim-rooter')
  autocmd! User RooterChDir call LoadLocalVimrc()
endif

call LoadLocalVimrc()
