if has_key(g:plugs, 'nvim-cmp')
  lua << EOF
local cmp = require('cmp')
cmp.setup{
  completion = {
    autocomplete = true
  },
  mapping = {
    ['<C-d>'] = cmp.mapping.scroll_docs(-4),
    ['<C-f>'] = cmp.mapping.scroll_docs(4),
    ['<C-Space>'] = cmp.mapping.complete(),
    ['<C-e>'] = cmp.mapping.close(),
    ['<CR>'] = cmp.mapping.confirm({
      behavior = cmp.ConfirmBehavior.Replace,
      select = true,
    }),
    ['<Tab>'] = cmp.mapping(cmp.mapping.select_next_item(), { 'i', 's' })
  },
  sources = cmp.config.sources({
    { name = 'nvim_lsp' },
  }, {
    { name = 'buffer' },
    { name = 'path' },
  }),
  snippet = {
    -- REQUIRED <-- WTF?
  },
}
EOF
  if has_key(g:plugs, 'lspkind')
    lua << EOF
local cmp = require('cmp')
local lspkind = require('lspkind')
cmp.setup {
  formatting = {
    format = lspkind.cmp_format(),
  },
}
EOF
  endif
endif
