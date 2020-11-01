if has_key(g:plugs, 'quickmenu.vim')
   call g:quickmenu#current(0)
   call g:quickmenu#append('Plugins', 'call quickmenu#toggle(1)', 'Show plugin menu', '', 99, '')

   call g:quickmenu#current(1)
   call g:quickmenu#header('Plugins')
   call g:quickmenu#append('Status', 'PlugStatus', 'Show status of plugins', '', 0, 's')
   call g:quickmenu#append('Update', 'PlugUpdate', 'Update/Install plugins', '', 0, 'u')
   call g:quickmenu#append('Diff', 'PlugDiff', 'Show changes to be installed', '', 0, 'd')
endif
" Map 'o' to open the plugin's remote URL (github page usually)
function! s:plug_gx()
    let line = getline('.')
    let sha  = matchstr(line, '^  \X*\zs\x\{7,9}\ze ')
    let name = empty(sha) ? matchstr(line, '^[-x+] \zs[^:]\+\ze:')
                \ : getline(search('^- .*:$', 'bn'))[2:-2]
    let uri  = get(get(g:plugs, name, {}), 'uri', '')
    if uri !~# 'github.com'
        return
    endif
    let repo = matchstr(uri, '[^:/]*/'.name)
    let url  = empty(sha) ? 'https://github.com/'.repo
                \ : printf('https://github.com/%s/commit/%s', repo, sha)
    call netrw#BrowseX(url, 0)
endfunction
augroup vim_plug_open
    autocmd! FileType vim-plug nmap <buffer> o :call <SID>plug_gx()<CR>
augroup END
" Try and install missing plugins on startup
augroup vim_plug_auto_install
   autocmd!
   autocmd VimEnter *
      \  if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
      \|   PlugInstall --sync | q
      \| endif
augroup END
" Map 'H' to open the plugin's docs
function! s:plug_doc()
    let name = matchstr(getline('.'), '^- \zs\S\+\ze:')
    if has_key(g:plugs, name)
        for doc in split(globpath(g:plugs[name].dir, 'doc/*.txt'), '\n')
            execute 'silent e' doc
        endfor
    endif
endfunction
augroup vim_plug_doc
    autocmd!
    autocmd FileType vim-plug nmap <buffer> H :call <SID>plug_doc()<cr>
augroup END
