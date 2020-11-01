" Fly Mode
let g:AutoPairsFlyMode = 0
" Default auto-pairing sets
let g:AutoPairs = {'(':')', '[':']', '{':'}',"'":"'",'"':'"', '`':'`'}
" Default auto-pairs off
let b:autopairs_enabled = 0


if has_key(g:plugs, 'quickmenu.vim') && has_key(g:plugs, 'auto-pairs')
   call g:quickmenu#current(0)
   call g:quickmenu#append('Toggle Auto-pairs', 'call AutoPairsToggle()', 'Toggle auto-pairs', '', 0, '')
endif
