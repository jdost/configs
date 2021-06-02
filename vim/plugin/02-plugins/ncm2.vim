if has_key(g:plugs, 'ncm2')
  " enable ncm2 for all buffers
  autocmd BufEnter * call ncm2#enable_for_buffer()

  " IMPORTANT: :help Ncm2PopupOpen for more information
  set completeopt=noinsert,menuone,noselect

  " CTRL-C doesn't trigger the InsertLeave autocmd . map to <ESC> instead.
  inoremap <C-c> <ESC>

  if ! has_key(g:plugs, 'supertab')
    inoremap <expr> <CR>    pumvisible() ? "\<C-y>\<CR>" : "\<CR>"
    inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
    inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
  endif
endif
