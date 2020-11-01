" Syntastic
function! s:lightline()
  SyntasticCheck
  call lightline#update()
endfunction

if has_key(g:plugs, 'lightline.vim') && has_key(g:plugs, 'syntastic')
   let g:lightline.component_expand.linter_error = 'SyntasticStatuslineFlag'
   let g:lightline.component_type.linter_error = 'error'
endif
