" Rebalance splits on resize
au VimResized * :wincmd =

" Set cursorline on focused window
augroup cline
   au!
   au WinLeave,InsertEnter * set nocursorline
   au WinEnter,InsertLeave * set cursorline
augroup END
