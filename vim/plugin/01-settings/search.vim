set ignorecase
set smartcase
set gdefault

set showmatch
set incsearch
" only set highlighting in colored terminals
if &t_Co > 2
   set hlsearch
endif

nnoremap / /\v
vnoremap / /\v

nnoremap <leader><space> :noh<cr>
nnoremap <tab> %
vnoremap <tab> %
" n and N center when jumping
nnoremap n nzzzv
nnoremap N Nzzzv

" Use `ripgrep` for grep if installed
if executable('rg')
   set grepprg=rg\ --color=never
endif
