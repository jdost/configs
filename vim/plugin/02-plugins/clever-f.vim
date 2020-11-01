" Whether `f` etc will match across new lines (0 = off)
let g:clever_f_across_no_line=0  " default
" Whether `f` will match both upper and lower case (0 = case sensitive)
let g:clever_f_ignore_case=0  " default
" Will match upper and lower case from lower case, but only upper case when
"   uppercase (0 = always case sensitive)
let g:clever_f_smart_case=0  " default
" When set to 1, `f` will always be to the right, and `F` always to the left,
"   when unset, `f` will always continue and `F` will always reverse original
"   input
let g:clever_f_fix_key_direction=0  " default
" Whether to display a prompt when in search mode
let g:clever_f_show_prompt=0  " default
" A "magic character" input to match symbol characters like (){}[]
let g:clever_f_chars_match_any_signs=';'  " default: ''
" Whether to highlight the current character when waiting for the target
"   character
let g:clever_f_mark_cursor=1  " default
" How long until the search mode expires, 0 means it never expires until a non
"   search character is input
let g:clever_f_timeout_ms=0  " default
