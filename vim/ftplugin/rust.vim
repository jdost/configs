if executable('rls') && has_key(g:plugs, 'vim-lsp')
   augroup asyncomplete_lsp_rust
      autocmd!
      " rustup component add rls rust-analysis rust-src
      au User lsp_setup call lsp#register_server({
         \ 'name': 'rls',
         \ 'cmd': {server_info->['rustup', 'run', 'stable', 'rls']},
         \ 'workspace_config': {'rust': {'clippy_preference': 'on'}},
         \ 'whitelist': ['rust'],
         \ })
   augroup END
 endif
