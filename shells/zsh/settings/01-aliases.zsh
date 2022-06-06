# global aliases {{{
alias serve="python3 -m http.server"

which term-info &>/dev/null && alias clear="clear;term-info"
# }}}
# fzf helpers {{{
{
    if ! which fzf &>/dev/null; then
        return 0
    fi

    igrep() {
        INITIAL_QUERY="$@"
        RG_PREFIX="rg --column --line-number --no-heading --color=always --smart-case "
        FZF_DEFAULT_COMMAND="$RG_PREFIX '$INITIAL_QUERY'" \
        fzf --bind "change:reload:$RG_PREFIX {q} || true" \
            --ansi --disabled --query "$INITIAL_QUERY" \
            --preview "cat {}" \
            --height=50% --layout=reverse
    }

    ## TODO: add `cd` wrapper, figure out interactive mode when no args
}
# }}}

# vim: ft=zsh foldmethod=marker
