if has_key(g:plugs, 'nvim-compe')
  set completeopt=menuone,noselect

  inoremap <silent><expr> <C-Space> compe#complete()
  " inoremap <silent><expr> <CR>      compe#confirm('<CR>')
  inoremap <silent><expr> <C-e>     compe#close('<C-e>')
  inoremap <silent><expr> <C-f>     compe#scroll({ 'delta': +4 })
  inoremap <silent><expr> <C-d>     compe#scroll({ 'delta': -4 })

  inoremap <silent><expr> <CR>      pumvisible() ? "\<C-y>\<CR>" : "\<CR>"
  inoremap <silent><expr> <Tab>     pumvisible() ? "\<C-n>" : "\<Tab>"
  inoremap <silent><expr> <S-Tab>   pumvisible() ? "\<C-p>" : "\<S-Tab>"

  lua << EOF
require('compe').setup{
  enabled = true;
  autocomplete = true;
  min_length = 1;
  debug = false;
  preselect = 'enable';
  source = {
    path = true;
    buffer = true;
    calc = true;
    nvim_lsp = true;
    nvim_lua = true;
  }
}
EOF
endif
