---
name: assembler-agent
description: Stage 6 — wires the cloned frontend, the generated API client, and the DB schema into one runnable repo with a documented run command.
role: developer
provider: claude_code
permissionMode: bypassPermissions
skills: ["bp-assemble", "bp-manifest"]
mcpServers:
  cao-mcp-server:
    type: stdio
    command: cao-mcp-server
    args: []
---
# Assembler agent
Load `bp-assemble`. Copy `frontend.repo_path` to `blueprint-out/app/`, drop in the
`api.client_path` client and `database.schema_prisma`, and wire the frontend's data
calls to the client per `dataflow.map`. Add `.env.example`, install deps, and verify
it builds. Write `assembly.repo_path`, `assembly.run_cmd`, `assembly.wired = true`;
set `status.assembly = "done"`.
