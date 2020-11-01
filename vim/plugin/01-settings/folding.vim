function! CustomFoldText() " {{{
   let line = getline(v:foldstart)

   let nucolwidth = &fdc + &number * &numberwidth
   "let windowwidth = winwidth(0) - nucolwidth - 3
   let windowwidth = &colorcolumn - 1
   let foldedlinecount = v:foldend - v:foldstart

   " expand tabs into spaces
   let onetab = strpart('          ', 0, &tabstop)
   let line = substitute(line, '\t', onetab, 'g')

   let line = strpart(line, 0, windowwidth - 2 -len(foldedlinecount))
   let fillcharcount = windowwidth - len(line) - len(foldedlinecount)
   return line . '…' . repeat(" ",fillcharcount) . foldedlinecount . '…' . ' '
endfunction " }}}

if has ('folding')
   set foldenable
   set foldmethod=indent
   set foldmarker={{{,}}}
   set foldcolumn=0
   set foldtext=CustomFoldText()
   set foldlevelstart=0
   hi Folded ctermfg=154 ctermbg=235

   nnoremap <Space> za
   vnoremap <Space> za
endif
