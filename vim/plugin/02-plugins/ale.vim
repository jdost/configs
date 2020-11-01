" The rest are defined in the ftplugin files
let g:ale_fixers = {
   \  '*': ['remove_trailing_lines', 'trim_whitespace'],
   \}

let g:ale_lint_delay = 500
" Run the ale fixers on save
let g:ale_fix_on_save = 1

"let g:ale_completion_enabled = 1
set omnifunc=ale#completion#OmniFunc

" Use a quickfix rather than loclist
let g:ale_set_loclist = 0
let g:ale_set_quickfix = 1
let g:ale_open_list = 1

" Cached failed linters/fixers
let g:ale_cache_executable_check_failures = 1
" Run tasks with a low priority
let g:ale_command_wrapper = 'nice -n5 %*'
" Don't care about `ALEInfo`
let g:ale_history_enabled = 0
let g:ale_history_log_output = 0

"keybindings
silent! if has_key(g:plugs, 'ale')
   nmap <silent> <C-k> <Plug>(ale_previous_wrap)
   nmap <silent> <C-j> <Plug>(ale_next_wrap)

   if has_key(g:plugs, 'quickmenu.vim')
      call g:quickmenu#current(0)
      call g:quickmenu#append('Toggle All Linting', 'AleToggle', 'Toggle Linting Globally', '', 0, '')
      call g:quickmenu#append('Toggle Local Linting', 'AleToggleBuffer', 'Toggle Linting Locally', '', 0, '')
   endif
endif

" Lightline stuff
function! s:is_linted() abort
   return get(g: 'ale_enabled', 0) == 1
      \ && getbufvar(bufnr(''), 'ale_linted', 0) > 0
      \ && ale#engine#IsCheckingBuffer(bufnr('')) == 0
endfunction

function! ale#llWarnings() abort
   if !s:is_linted()
      return ''
   endif
   let l:counts = ale#statusline#Count(bufnr(''))
   let l:warning_count = (l:counts.total - l:counts.error - l:counts.style_error)
   return  l:warning_count == 0 ? '' : printf('W %d', warning_count)
endfunction

function! ale#llErrors() abort
   if !s:is_linted()
      return ''
   endif
   let l:counts = ale#statusline#Count(bufnr(''))
   let l:error_count = (l:counts.error + l:counts.style_error)
   return l:error_count == 0 ? '' : printf('E %d', error_count)
endfunction

function! ale#llOk() abort
   if !s:is_linted()
      return ''
   endif
   return ale#statusline#Count(bufnr('')).total == 0 ? 'OK' : ''
endfunction

function! ale#llChecking() abort
   return ale#engine#IsCheckingBuffer(bufnr('')) ? 'Linting...' : ''
endfunction

" We don't have airline, lightline is used instead
let g:airline#extensions#ale#enabled = 0

silent! if has_key(g:plugs, 'ale') && has_key(g:plugs, 'lightline.vim')
   let g:lightline.component_expand.linter_status = 'ale#llChecking'
   let g:lightline.component_type.linter_status = 'middle'
   let g:lightline.component_expand.linter_ok = 'ale#llOk'
   let g:lightline.component_type.linter_ok = 'middle'
   let g:lightline.component_expand.linter_warning = 'ale#llWarning'
   let g:lightline.component_type.linter_warning = 'warning'
   let g:lightline.component_expand.linter_error = 'ale#llError'
   let g:lightline.component_type.linter_error = 'error'

   augroup ale_lightline
      autocmd!
      autocmd User ALEJobStarted call lightline#update()
      autocmd User ALELintPost call lightline#update()
      autocmd User ALEFixPost call lightline#update()
   augroup END
endif
