" Source lines in vimscript
vnoremap <leader>S y:execute @@<cr>:echo 'Sourced selection.'<cr>
nnoremap <leader>S ^vg_y:execute @@<cr>:echo 'Sourced line.'<cr>

setlocal tabstop=2
setlocal shiftwidth=2

if has_key(g:plugs, 'nvim-treesitter')
  TSInstallIfNot vim
end
