silent! if has_key(g:plugs, 'nvim-treesitter')
  lua << EOF
require('nvim-treesitter.configs').setup {
  highlight = {
    enable = true,
    custom_captures = {
    },
    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
    additional_vim_regex_highlighting = false,
    disable = function(lang, buf)
      local max_filesize = 128 * 1024 -- 128 KB
      local ok, stats = pcall(vim.loop.fs_stat, vim.api.nvim_buf_get_name(buf))
      if ok and stats and stats.size > max_filesize then
        return true
      end
    end,
  },
}

vim.api.nvim_create_user_command(
  'TSInstallIfNot',
  function(opts)
    local lang = opts.fargs[1]
    local treesitter = require("nvim-treesitter.info")
    local installed = false
    for _, language in pairs(treesitter.installed_parsers()) do
      if language == lang then
        installed = true
        break
      end
    end
    if not installed then
      vim.cmd("TSInstall "..lang)
    end
  end,
  {nargs = 1}
)
EOF

  if has_key(g:plugs, 'quickmenu.vim')

    function! TSInstallCurrent()
      execute ':TSInstall ' . &filetype
    endfunction

    call g:quickmenu#current(0)
    call g:quickmenu#append('Install TS Language Support', 'call TSInstallCurrent()', 'Install TreeSitter plugin for current language', '', 0, '')
  endif
endif
