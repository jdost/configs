" auto calculate the guide colors
let g:indent_guides_auto_colors=1
" amount of the indentation that gets colored (0 for all)
let g:indent_guides_guide_size=0
" indentation level to begin coloring
let g:indent_guides_start_level=1
" enable plugin by default
let g:indent_guides_enable_on_vim_startup=1

if has_key(g:plugs, 'vim-indent-guides')
   " keymapping
   nnoremap <leader>ig <Plug>IndentGuidesToggle

   if has_key(g:plugs, 'quickmenu.vim')
      call g:quickmenu#current(0)
      call g:quickmenu#append('Toggle indent guides', 'IndentGuidesToggle', 'Toggle indent guides', '', 1, '')
   endif
endif
