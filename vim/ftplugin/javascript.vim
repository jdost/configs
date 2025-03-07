" Tab sizes
setlocal shiftwidth=2
setlocal tabstop=2
" Folding
setlocal foldmethod=marker
setlocal foldmarker={,}
" Completion
setlocal omnifunc=javascriptcomplete#CompleteJS
" Opening a function doesn't unfold
"inoremap <buffer> {<cr> {}<left><cr><space><space>.<cr><esc>kA<bs>

" Abbreviations
iabbrev fun function

if has_key(g:plugs, 'nvim-treesitter')
  " Use treesitter for folding logic
  setlocal foldmethod=expr
  setlocal foldexpr=nvim_treesitter#foldexpr()

  TSInstallIfNot javascript
end
