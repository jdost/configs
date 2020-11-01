" if autocmd exists, setup auto settings {{{
if has("autocmd")
   " set default width for text documents
   autocmd FileType text setlocal textwidth=80
   " return to last known *valid* cursor position
   autocmd BufReadPost *
     \ if line("'\"") > 1 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif
   "if exists("+omnifunc")
   "   autocmd FileType *
   "     \ if &omnifunc == "" |
   "     \   setlocal omnifunc = syntanxcomplete#Complete |
   "     \ endif
   "endif
endif " }}}
" tab handling
set expandtab
set shiftwidth=3
set tabstop=3
set smarttab
" indentation handling
set autoindent
set smartindent
set nowrap

set formatoptions=cn

" Filetype setup
au BufNewFile,BufRead *.md set filetype=markdown
au BufNewFile,BufRead *.go set filetype=go
au BufNewFile,BufRead *.graphql,*.graphqls,*.gql set filetype=graphql

if !has('conceal')
   finish
endif
" Conceals (change long names into shorthand symbols)
"syntax keyword concealKeyword function conceal cchar=ϝ
"syntax match concealOp "<=" conceal cchar=≤
"syntax match concealOp ">=" conceal cchar=≥
"syntax match concealOp "==" conceal cchar=≡
"syntax match concealOp "!=" conceal cchar=≠

set conceallevel=2
