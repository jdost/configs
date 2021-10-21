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
  },
}
EOF
  if has_key(g:plugs, 'quickmenu.vim')

    function! TSInstallCurrent()
      execute ':TSInstall ' . &filetype
    endfunction

    call g:quickmenu#current(0)
    call g:quickmenu#append('Install TS Language Support', 'call TSInstallCurrent()', 'Install TreeSitter plugin for current language', '', 0, '')
  endif
endif
