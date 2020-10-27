# VI mode
bindkey -v
# Key bindings
bindkey "${terminfo[khome]}"  beginning-of-line    # Home
bindkey "${terminfo[kend]}"   end-of-line          # End
bindkey "${terminfo[kpp]}"    beginning-of-history # PageUp
bindkey "${terminfo[knp]}"    end-of-history       # PageDown
bindkey "${terminfo[kdch1]}"  delete-char          # Del
bindkey "^[0c"   forward-word         # Ctrl + Right
bindkey "^[0d"   backward-word        # Ctrl + Left

# vim bindings
bindkey -M viins "jj" vi-cmd-mode # use jj for escape
bindkey -M vicmd "/" history-incremental-search-backward
bindkey -M vicmd "?" history-incremental-search-forward
bindkey -M vicmd "//" history-beginning-search-backward
bindkey -M vicmd "??" history-beginning-search-forward

bindkey -M vicmd "q" push-line
bindkey -M vicmd "!" edit-command-output

autoload -Uz edit-command-line
bindkey -M vicmd 'v' edit-command-line

# converts ... -> ../.. and backwards
function rationalize_dot () {
   local MATCH # keep regex match from leaking into the environment
   if [[ $LBUFFER =~ '(^|/| |      |'$'\n''|\||;|&)\.\.$' ]]; then
      LBUFFER+=/
      zle self-insert
      zle self-insert
   else
      zle self-insert
   fi
}
zle -N rationalize_dot
bindkey . rationalize_dot
bindkey -M isearch . self-insert

function unrationalize_dot () {
   local MATCH # keep regex match from leaking into the environment
   if [[ $LBUFFER =~ '(^|/| |      |'$'\n''|\||;|&)\.\.$' ]]; then
      zle backward-delete-char
      zle backward-delete-char
      if [[ $MATCH =~ '^/' ]]; then
         zle backward-delete-char
      fi
   else
      zle backward-delete-char
   fi
}
zle -N unrationalize_dot
bindkey "^h" unrationalize_dot
bindkey "^?" unrationalize_dot

# lets Ctrl-Z in shell attempt to foreground
function fancy-ctrl-z () {
   if [[ $#BUFFER -eq 0 ]]; then
      BUFFER="fg"
      zle accept-line
   else
      zle push-input
      zle clear-screen
   fi
}
zle -N fancy-ctrl-z
bindkey '^Z' fancy-ctrl-z

function sudo-command-line () {
   [[ -z $BUFFER ]] && zle up-history
   if [[ $BUFFER == sudo\ * ]]; then
      LBUFFER="${LBUFFER#sudo }"
   else
      LBUFFER="sudo $LBUFFER"
   fi
}
zle -N sudo-command-line
# Defined shortcut keys: [Esc] [Esc]
bindkey -M viins "\e\e" sudo-command-line
