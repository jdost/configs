let g:committia_hooks = {}
let g:committia_open_only_vim_starting = 0

function! g:committia_hooks.edit_open(info)
   setlocal spell

   " launch in insert if nothing prepopulated
   if a:info.vcs ==# 'git' && getline(1) ==# ''
      startinsert
   endif

   " Use PageUp/PageDown to scroll from message window
   imap <buffer> <PageDown>   <Plug>(committia-scroll-diff-down-half)
   imap <buffer> <PageUp>     <Plug>(committia-scroll-diff-up-half)
   imap <buffer> <S-PageDown> <Plug>(committia-scroll-diff-down-page)
   imap <buffer> <S-PageUp>   <Plug>(committia-scroll-diff-up-page)

   nmap <buffer> <PageDown>   <Plug>(committia-scroll-diff-down-half)
   nmap <buffer> <PageUp>     <Plug>(committia-scroll-diff-up-half)
   nmap <buffer> <S-PageDown> <Plug>(committia-scroll-diff-down-page)
   nmap <buffer> <S-PageUp>   <Plug>(committia-scroll-diff-up-page)
endfunction
