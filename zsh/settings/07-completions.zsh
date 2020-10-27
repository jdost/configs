export COMPDUMPFILE=$XDG_CACHE_HOME/zcompdump

c1=$'\e[1;33m'
c3=$'\e[0;31m'
reset_color=$'\e[0;0m'

# autocompletion look
zstyle ':completion:*:descriptions'       format "%{$c1%}%d%{$reset_color%}"
zstyle ':completion:*:corrections'        format "%{$c3%}%d%{$reset_color%}"
zstyle ':completion:*:messages'           format "%{$c1%}%d%{$reset_color%}"
zstyle ':completion:*:warnings'           format "%{$c1%}%d%{$reset_color%}"
# completion settings
zstyle ':completion:*'                       accept-exact '*(N)'
zstyle ':completion:*'                       separate-sections 'yes'
#zstyle ':completion:*'                       list-dirs-first true
#zstyle ':completion:*:default'               list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*'                       menu select=200
zstyle ':completion:*'                       squeeze-slashes true
# Include ZSH completion git repo
[[ ! -d "$PLUGIN_DIR/custom_completions" ]] && mkdir -p "$PLUGIN_DIR/custom_completions"
fpath=($PLUGIN_DIR/custom_completions $fpath)
compinit -i
# man completion
zstyle ':completion:*:manuals'    separate-sections true
zstyle ':completion:*:manuals.*'  insert-sections   true
zstyle ':completion:*:man:*'      menu yes select
# vcs_info
zstyle ':vcs_info:*'                      enable git hg
# ssh completion
zstyle -s ':completion:*:hosts' hosts _ssh_config
[[ -r ~/.ssh/config ]] && _ssh_config+=($(cat ~/.ssh/config | sed -ne 's/Host[=\t ]//p'))
zstyle ':completion:*:hosts' hosts $_ssh_config
# check-for-changes can be really slow.
# you should disable it, if you work with large repositories
zstyle ':vcs_info:*' check-for-changes true
zstyle ':vcs_info:*' unstagedstr '%F{62}D%F{237}%f'  # display ¹ if there are unstaged changes
zstyle ':vcs_info:*' stagedstr '%F{62}S%F{237}%f'     # display ² if there are staged changes
zstyle ':vcs_info:*' actionformats "${FMT_BRANCH}${FMT_ACTION}" "${FMT_PATH}"
zstyle ':vcs_info:*' formats       "${FMT_BRANCH}"              "${FMT_PATH}"
zstyle ':vcs_info:*' nvcsformats   ""                           "%~"
zstyle ':vcs_info:git*+set-message:*' hooks git-st
# sudo
zstyle ':completion:*:sudo:*' command-path /usr/local/sbin /usr/local/bin  \
   /usr/sbin /usr/bin /sbin /bin /usr/X11R6/bin
# application specific completion
zstyle ':completion:*' group-name            ''
 # mplayer
zstyle ':completion:*:*:mplayer:*'           tag-order files
zstyle ':completion:*:*:mplayer:*'           file-patterns   \
      '*.(rmvb|mkv|mpg|wmv|mpeg|avi|flv|mp3|mp4|flac|ogg):video' \
      '*:all-files' '*(-/):directories'
 # vim
zstyle ':completion:*:*:(vim|vimdiff):*:*files' \
  ignored-patterns '*~|*.(old|bak|zwc|viminfo|rxvt-*|zcompdump)|pm_to_blib|cover_db|blib' \
  file-sort modification
zstyle ':completion:*:*:(vim|vimdiff):*' \
  file-sort modification
zstyle ':completion:*:*:(vim|vimdiff):*' \
  tag-order files
# pdf
zstyle ':completion:*:*:(llpp|apvlv|zathura):*'             tag-order files
zstyle ':completion:*:*:(llpp|apvlv|zathura):*'             file-patterns '*.pdf'
# vim: ft=zsh tw=2
