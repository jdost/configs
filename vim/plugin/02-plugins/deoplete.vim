let g:deoplete#enable_at_startup = 1
let g:deoplete#enable_smart_case = 1

silent! if has_key(g:plugs, 'deoplete.nvim')
   inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
   inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
   inoremap <expr> <CR>    pumvisible() ? deoplete#mappings#close_popup() : "\<CR>"
endif
