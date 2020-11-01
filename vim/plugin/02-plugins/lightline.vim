let g:lightline.active.left = [
   \   [ 'mode', 'paste' ],
   \   [ 'fugitive', 'filename' ],
   \   [ 'ctrlp' ]
   \ ]

let g:lightline.active.right = [
   \   [ 'linter_status', 'linter_status', 'linter_error', 'linter_warning', 'linter_ok' ],
   \   [ 'lineinfo', 'percent' ],
   \   [ 'fileformat', 'fileencoding', 'filetype' ]
   \ ]

let g:lightline.component.paste = '%{&paste?"P":""}'
let g:lightline.component_function.filename = 'LightlineFilename'

function! LightlineReadonly()
   return &ft !~? 'help' && &readonly ? 'x' : ''
endfunction

function! LightlineModified()
   return &ft =~ 'help' ? '' : &modified ? '+' : &modifiable ? '' : '-'
endfunction

function! LightlineFilename()
   let fname = expand('%:t')
   return  fname == 'ControlP' ? g:lightline#ctrlp#item :
         \ fname == '__Tagbar__' ? g:lightline.fname :
         \ ('' != LightlineReadonly() ? LightlineReadonly() . ' ' : '') .
         \ ('' != expand('%:t') ? expand('%:t') : '[No Name]') .
         \ ('' != LightlineModified() ? ' ' . LightlineModified() : '')
endfunction
