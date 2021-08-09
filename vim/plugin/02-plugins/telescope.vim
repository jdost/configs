silent! if has_key(g:plugs, 'telescope.nvim')
  nnoremap <C-P> <cmd>Telescope buffers<cr>

  " Disable autocomplete plugins for the prompt
  if has_key(g:plugs, 'ncm2')
    autocmd FileType TelescopePrompt call ncm2#disable_for_buffer()
  elseif has_key(g:plugs, 'asyncomplete')
    autocmd FileType TelescopePrompt call asyncomplete#disable_for_buffer()
  endif
  lua << EOF
local actions = require('telescope.actions')
local action_state = require('telescope.actions.state')
local cycle_lookup = {
  ["Buffers"] = "find_files",
  ["Find Files"] = "live_grep",
  ["Live Grep"] = "buffers",
}
local cycle_pickers = function()
  -- Get the current picker so we can lookup the next picker in the cycle
  local prompt_bufnr = vim.api.nvim_get_current_buf()
  local current_picker = action_state.get_current_picker(prompt_bufnr)
  -- Need to capture state for the next picker before we close this one
  local next_picker = require('telescope.builtin')[cycle_lookup[current_picker.prompt_title]]
  local buffer = current_picker:_get_prompt()
  -- Close but keep in insert mode
  actions._close(prompt_bufnr, true)
  -- Launch the next picker in the cycle
  next_picker({ })
  -- Grab the new picker to finish setting it up
  prompt_bufnr = vim.api.nvim_get_current_buf()
  current_picker = action_state.get_current_picker(prompt_bufnr)
  current_picker:reset_prompt(buffer)
end
require('telescope').setup{
  defaults = {
    theme = "ivy",
    default_text = "",
    mappings = {
      i = {
        ["<esc>"] = actions.close,
        ["<C-f>"] = cycle_pickers,
      },
    },
  },
  pickers = {
    buffers = { theme = "ivy", },
    find_files = { theme = "ivy", },
    git_files = { theme = "ivy", },
    live_grep = { theme = "ivy", },
  },
}
EOF
endif
