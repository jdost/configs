if has_key(g:plugs, 'nvim-lint')
  lua << EOF
    local lint = require('lint')

    local tf_linters = {}

    if vim.fn.executable('tfsec') == 1 then
      table.insert(tf_linters, 'tfsec')
    end

    if vim.fn.executable('tflint') == 1 then
      table.insert(tf_linters, 'tfsec')
    end

    lint.linters_by_ft['terraform'] = tf_linters
EOF
endif

if has_key(g:plugs, 'conform.nvim')
  lua << EOF
    local conform = require('conform')
    conform.formatters_by_ft.terraform = { 'terraform_fmt' }
EOF
endif
