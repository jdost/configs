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

# utilize fzf if installed
{
    if ! which fzf &>/dev/null; then
        return 0
    fi

    __fzfcmd() {
        [ -n "$TMUX_PANE" ] && { [ "${FZF_TMUX:-0}" != 0 ] || [ -n "$FZF_TMUX_OPTS" ]; } &&
        echo "fzf-tmux ${FZF_TMUX_OPTS:--d${FZF_TMUX_HEIGHT:-40%}} -- " || echo "fzf"
    }

    fzf-history-widget() {
        local selected num
        setopt localoptions noglobsubst noposixbuiltins pipefail no_aliases 2> /dev/null
        selected=( $(fc -rl 1 | perl -ne 'print if !$seen{(/^\s*[0-9]+\**\s+(.*)/, $1)}++' |
            FZF_DEFAULT_OPTS="--height ${FZF_TMUX_HEIGHT:-40%} $FZF_DEFAULT_OPTS -n2..,.. --tiebreak=index --bind=ctrl-r:toggle-sort,ctrl-z:ignore $FZF_CTRL_R_OPTS --query=${(qqq)LBUFFER} +m" $(__fzfcmd)) )
        local ret=$?
        if [ -n "$selected" ]; then
            num=$selected[1]
            if [ -n "$num" ]; then
                zle vi-fetch-history -n $num
            fi
        fi
        zle reset-prompt
        return $ret
    }

    zle -N fzf-history-widget
    bindkey -M viins "^R" fzf-history-widget
    bindkey -M vicmd "?" fzf-history-widget
}
