if has('nvim-0.5')
  lua << EOF
  vim.diagnostic.config({
    virtual_text = {
      source = "always",
      prefix = 'x',
    },
    severity_sort = true,
    float = {
      source = "always",
    },
  })
EOF
endif
