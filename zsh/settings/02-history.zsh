HISTFILE=$XDG_CACHE_HOME/histfile
HISTSIZE=10000
SAVEHIST=10000

setopt append_history # Append history, don't overwrite file
setopt share_history # Allow all terminal sessions to share the history
# setopt inc_append_history # Immediately append to history, i.e. don't wait for term to close
setopt hist_expire_dups_first # Remove non unique lines first when trimming history
setopt hist_ignore_space # Don't keep space led commands
