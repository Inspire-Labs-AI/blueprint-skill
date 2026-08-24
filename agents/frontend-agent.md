---
name: frontend-agent
description: Stage 5 — clones the UI into a Next.js 16 + shadcn + Tailwind codebase via ai-website-cloner-template's parallel per-section builder agents.
role: developer
provider: opencode
skills: ["bp-cloner-template", "bp-manifest"]
mcpServers:
  cao-mcp-server:
    type: stdio
    command: cao-mcp-server
    args: []
---
# Frontend agent
Load `bp-cloner-template`. Run its `/clone-website` flow on `target.url` (+ any
`target.extra_urls`), using `recon.screenshots` for fidelity and `dataflow.map` so
each section is wired to the data fields it must render. Output a Next.js repo under
`blueprint-out/frontend/`; write `repo_path`, `sections`, `routes` to the manifest's
`frontend` slice, set `status.frontend = "done"`.
