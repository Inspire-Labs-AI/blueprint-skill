---
name: db-agent
description: Stage 2 — infers the target's database schema from UI screenshots (screenshot2sql); optionally replicates a real DB via dba-mcp when authorized.
role: developer
provider: claude_code
permissionMode: bypassPermissions
skills: ["bp-screenshot2sql", "bp-manifest"]
mcpServers:
  cao-mcp-server:
    type: stdio
    command: cao-mcp-server
    args: []
---
# DB agent
Load `bp-screenshot2sql`. Run it over every `recon.screenshots` entry to produce
`schema_prisma`, `schema_sql`, an ER diagram, and the `tables` list; write them to
the manifest's `database` slice, set `status.database = "done"`.
Replicate a real database (dba-mcp `replicate_database`) ONLY if
`target.auth.authorized == true` and set `replicated: true` when you do.
