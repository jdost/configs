setlocal wrap
setlocal shiftwidth=2
setlocal tabstop=2
setlocal nolist
setlocal linebreak
setlocal foldmarker={{{,}}}

let g:TrimOnSave = 0

silent! if has_key(g:plugs, 'neocomplcache')
   "let g:neocomplcache_enable_at_startup = 0
   if !exists('g:neocomplcache_disabled_sources_list')
      let g:neocomplcache_disabled_sources_list = {}
   endif
   let g:neocomplcache_disabled_sources_list.markdown =
      \ ['buffer_complete', 'member_complete']
endif

" spell check
setlocal spell
set dictionary=/usr/share/dict/words
set spellfile=~/.local/custom-dictionary.utf-8.add

" codeblocks
let g:markdown_fenced_languages = ['python', 'javascript', 'js=javascript',
         \ 'json=javascript', 'ruby', 'css', 'less', 'sass', 'xml', 'html',
         \ 'hs=haskell', 'haskell', 'zsh', 'sh', 'bash=sh', 'vim' ]
let g:vim_markdown_fenced_languages = ['python', 'javascript', 'js=javascript',
         \ 'json=javascript', 'ruby', 'css', 'less', 'sass', 'xml', 'html',
         \ 'hs=haskell', 'haskell', 'zsh', 'sh', 'bash=sh', 'vim' ]

" vim-markdown
let g:vim_markdown_no_default_key_mappings = 1
set conceallevel=2
let g:vim_markdown_new_list_item_indent = 2
let g:vim_markdown_strikethrough = 1
let g:vim_markdown_folding_disabled = 1

" display stuff
silent! if has_key(g:plugs, 'goyo.vim')
   :Goyo
endif

silent! if has_key(g:plugs, 'vim-pencil')
   :HardPencil
   let g:pencil#autoformat = 0
endif
