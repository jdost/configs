" if 256 colors use a colorscheme
if &t_Co >= 256

   if has_key(g:plugs, 'badwolf')
      colorscheme badwolf
   elseif has_key(g:plugs, 'seoul256.vim')
      let g:seoul256_background = 235
      colorscheme seoul256
   endif
   syntax on

   hi Normal ctermbg=none
   hi Nontext ctermbg=none
endif

set synmaxcol=300

set encoding=utf-8
" Line numbering
set number
set numberwidth=5
" Special characters in a file
set list
set listchars=tab:>\ ,trail:-,eol:¬
set fillchars=vert:┃ "║

set ttyfast
set lazyredraw

set cursorline
set colorcolumn=85
" netrw
let g:netrw_list_hide= ".git,*\.pyc,*\.png"

" cursor changes based on mode
if &term == 'xterm-256color' || &term == 'rxvt-unicode-256color' || &term == 'screen-256color' || &term == 'screen-256color-it'
   let &t_SI = "\<Esc>[5 q"
   let &t_EI = "\<Esc>[1 q"
   " urxvt has not implemented the bar cursor until 9.21, if that's the case, use an underbar: let &t_SI = "\<Esc>[3 q"
endif

set scrolloff=5
execute 'nnoremap H H' . &l:scrolloff . 'k'
execute 'vnoremap H H' . &l:scrolloff . 'k'
execute 'nnoremap L L' . &l:scrolloff . 'j'
execute 'vnoremap L L' . &l:scrolloff . 'j'

command! -nargs=? -complete=file V :call s:Vsplit( '<args>' )
command! -nargs=? -complete=file S :call s:Ssplit( '<args>' )

function! s:Vsplit(files)
   echom a:files
   if a:files == ""
      vsplit .
   else
      execut "vsplit " . a:files
   endif
endfunction

function! s:Ssplit(files)
   echom a:files
   if a:files == ""
      split .
   else
      execut "split " . a:files
   endif
endfunction
