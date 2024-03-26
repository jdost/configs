silent! if has_key(g:plugs, 'vim-vsnip')
  let g:vsnip_namespace = 'snip_'
  "imap <silent><expr> <Tab> vsnip#available(1)    ? '<Plug>(vsnip-expand-or-jump)' : minx#expand('<LT>Tab>')
  "smap <silent><expr> <Tab> vsnip#jumpable(1)     ? '<Plug>(vsnip-jump-next)'      : minx#expand('<LT>Tab>')
  "imap <silent><expr> <S-Tab> vsnip#available(-1) ? '<Plug>(vsnip-jump-prev)'      : minx#expand('<LT>S-Tab>')
  "smap <silent><expr> <S-Tab> vsnip#available(-1) ? '<Plug>(vsnip-jump-prev)'      : minx#expand('<LT>S-Tab>')
endif
