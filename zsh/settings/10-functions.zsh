reload () { source $ZSHRC; clear }
function '#' () { }

# creates a custom name for the current directory {{{
[[ ! -e $ZSH_SETTINGS_DIR/99-directories.zsh ]] && touch $ZSH_SETTINGS_DIR/99-directories.zsh
namedir () {
   echo "$1=$PWD ;  : ~$1" >> $ZSH_SETTINGS_DIR/99-directories.zsh
   . $ZSH_SETTINGS_DIR/99-directories.zsh
} # }}}

# Terminal color tests {{{
color () {
   for i; do
      print -P -- "\033[48;5;${i}m $i \033[0m"
   done
} # }}}

# vim: ft=zsh:foldmethod=marker
