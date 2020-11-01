function! s:smart_cr()
   if pumvisible()
      return asyncomplete#menu_selected() ? asyncomplete#close_popup() : asyncomplete#cancel_popup() . "\<CR>"
   else
      return "\<CR>"
   endif
endfunction

function! ToggleAsyncomplete()
   if b:asyncomplete_enable == 1
      call asyncomplete#disable_for_buffer()
   else
      call asyncomplete#enable_for_buffer()
   endif
endfunction

if has_key(g:plugs, 'asyncomplete.vim')
   let g:asyncomplete_default_refresh_pattern = '\(\k\+$\|\.$\)'
   let g:asyncomplete_smart_completion = 1
   let g:asyncomplete_auto_popup = 1
   let g:asyncomplete_remove_duplicates = 1

   inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
   inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
   inoremap <expr> <CR>    <SID>smart_cr()

   autocmd! CompleteDone * if pumvisible() == 0 | pclose | endif

   if has_key(g:plugs, 'quickmenu.vim')
      call g:quickmenu#current(0)
      call g:quickmenu#append('Toggle autocomplete', 'call ToggleAsyncomplete()', '', '', 1, '')
   endif
endif

" asyncomplete-buffer
if has_key(g:plugs, 'asyncomplete-buffer.vim') && has_key(g:plugs, 'asyncomplete.vim')
   let g:asyncomplete_buffer_clear_cache = 1

   augroup asyncomplete_buffer
      autocmd!
      autocmd User asyncomplete_setup call asyncomplete#register_source(asyncomplete#sources#buffer#get_source_options({
         \ 'name': 'buffer',
         \ 'whitelist': ['*'],
         \ 'blacklist': ['go', 'markdown', 'md'],
         \ 'completor': function('asyncomplete#sources#buffer#completor'),
         \ 'config': {
         \    'max_buffer_size': 50000,
         \  },
         \ }))
   augroup END
endif

" tmux-complete
if has_key(g:plugs, 'tmux-complete.vim') && has_key(g:plugs, 'asyncomplete.vim')
   let g:tmuxcomplete#asyncomplete_source_options = {
      \ 'name':      'tmuxcomplete',
      \ 'whitelist': ['*'],
      \ 'config': {
      \     'splitmode':      'words',
      \     'filter_prefix':   1,
      \     'show_incomplete': 1,
      \     'sort_candidates': 0,
      \     'scrollback':      0,
      \     'truncate':        0
      \     }
      \ }
endif

" asyncomplete-file
if has_key(g:plugs, 'asyncomplete-file.vim') && has_key(g:plugs, 'asyncomplete.vim')
   augroup asyncomplete_file
      autocmd!
      autocmd User asyncomplete_setup call asyncomplete#register_source(asyncomplete#sources#file#get_source_options({
         \ 'name': 'file',
         \ 'whitelist': ['*'],
         \ 'blacklist': ['markdown', 'md'],
         \ 'priority': 10,
         \ 'completor': function('asyncomplete#sources#file#completor'),
         \ }))
   augroup END
endif

" asyncomplete-necosyntax
if has_key(g:plugs, 'asyncomplete-necosyntax.vim') && has_key(g:plugs, 'asyncomplete.vim')
   augroup asyncomplete_necosyntax
      autocmd!
      autocmd User asyncomplete_setup call asyncomplete#register_source(asyncomplete#sources#necosyntax#get_source_options({
         \ 'name': 'necosyntax',
         \ 'whitelist': ['*'],
         \ 'completor': function('asyncomplete#sources#necosyntax#completor'),
         \ }))
   augroup END
endif
