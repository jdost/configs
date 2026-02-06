if has_key(g:plugs, 'sllm.nvim')
  lua << EOF
    require('sllm').setup({
      default_model = "anthropic/claude-sonnet-4-5",
      --default_mode = "sllm_read",
      keymaps = false,
    })
EOF
  command LLMAsk :lua require('sllm').ask_llm()
  command Ask :lua require('sllm').ask_llm()
  command -nargs=? LLMRun :lua require('sllm').run_command('<args>')
endif
