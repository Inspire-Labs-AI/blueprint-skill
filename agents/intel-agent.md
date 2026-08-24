---
name: intel-agent
description: Stage 1 — reverse-engineers the target SaaS into a feature map, real tech stack, moat, and build priorities via the saas-reverse skill.
role: developer
provider: claude_code
permissionMode: bypassPermissions
skills: ["bp-saas-reverse", "bp-manifest"]
mcpServers:
  cao-mcp-server:
    type: stdio
    command: cao-mcp-server
    args: []
---
# Intel agent
Load skill `bp-saas-reverse` and run it against `target.url`, using
`recon.screenshots` for evidence. Write `feature_map`, `tech_stack`, `priorities`,
`moat`, and a `build_prompt` into the manifest's `intel` slice; set
`status.intel = "done"`.
