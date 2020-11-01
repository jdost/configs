let g:ctrlp_cmd = "CtrlPBuffer"
" Custom ignores
let g:ctrlp_custom_ignore = {
\     'dir': '\v[\/]\.(git|hg)$',
\     'file': '\v\.(pyc|o|hi)$'
\  }
" Caching
let g:ctrlp_clear_cache_on_exit = 1
let g:ctrlp_cache_dir = $XDG_CACHE_HOME.'/vim/ctrlp/'
let g:ctrlp_max_depth = 10
" Keymap
let g:ctrlp_prompt_mappings = {
\     'AcceptSelection("v")': ['<C-Enter>']
\  }
" MRU
let g:ctrlp_mruf_relative = 1
let g:ctrlp_mruf_max = 50
" Search Behavior
let g:ctrlp_lazy_update = 500 " ms
let g:ctrlp_working_path_mode = 'ra'
" Indexing improvements
if executable('rg')
   let g:ctrlp_use_caching = 0
   let g:ctrlp_user_command = 'rg %s --files --color=never --glob ""'
else
   let g:ctrlp_use_caching = 1
   let g:ctrlp_user_command = ['.git',
   \  'cd %s && git ls-files . -co --exclude-standard', 'find %s -type f']
endif

" CtrlP
function! ctrlp#llMark()
   if expand('%:t') =~ 'ControlP'
      call lightline#link('iR'[g:lightline#ctrlp#regex])
      return lightline#concatenate([g:lightline#ctrlp#prev, g:lightline#ctrlp#item
         \ , g:lightline#ctrlp#next], 0)
   else
      return ''
   endif
endfunction

let g:ctrlp_status_func = {
  \ 'main': 'ctrlp#llStatus1',
  \ 'prog': 'ctrlp#llStatus2',
  \ }

function! ctrlp#llStatus1(focus, byfname, regex, prev, item, next, marked)
   let g:lightline#ctrlp#regex = a:regex
   let g:lightline#ctrlp#prev = a:prev
   let g:lightline#ctrlp#item = a:item
   let g:lightline#ctrlp#next = a:next
   return lightline#statusline(0)
endfunction

function! ctrlp#llStatus2(str)
   return lightline#statusline(0)
endfunction

if has_key(g:plugs, 'lightline.vim') && has_key(g:plugs, 'ctrlp.vim')
   let g:lightline.component_function.ctrlp = 'ctrlp#llMark'
endif
