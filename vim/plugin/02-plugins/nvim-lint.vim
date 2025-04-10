silent! if has_key(g:plugs, 'nvim-lint')
  lua << EOF
local lint = require('lint')

-- Initialize, but populate in filetype settings
lint.linters_by_ft = { }

-- Hook to run linters on write
vim.api.nvim_create_autocmd({ "BufWritePost" }, {
  callback = function()
    require("lint").try_lint()
  end,
})
EOF
endif
