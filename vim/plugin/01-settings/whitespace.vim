let g:TrimOnSave = 1

function TrimWhiteSpace()
   " Save position and searches
   let _s=@/
   let l = line(".")
   let c = col(".")
   " Perform the trim
   %s/\s*$//
   " Restore saves
   let @/ = _s
   call cursor(l, c)
endfunction

function AutoTrim()
   if g:TrimOnSave
      call TrimWhiteSpace()
   endif
endfunction

autocmd BufWritePre * :call AutoTrim()
nnoremap <leader>W :call TrimWhiteSpace()<cr>
