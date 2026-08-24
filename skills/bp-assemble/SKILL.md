---
name: bp-assemble
description: Stage 6 wiring. Merges the cloned frontend, generated API client, and DB schema into one runnable repo and verifies it builds.
---
# bp-assemble — the glue (only genuinely new code)

1. Copy `frontend.repo_path` → `blueprint-out/app/`.
2. Drop the `api.client_path` typed client into `app/lib/api/`.
3. Drop `database.schema_prisma` into `app/prisma/schema.prisma`.
4. Using `dataflow.map`, replace each section's mock/placeholder data calls with the
   real client method for its `api_endpoint`. Where `api.live=false`, leave the client
   stubbed but typed (compiles, returns fixtures).
5. Write `app/.env.example` (API base URL, DB URL) — never real secrets.
6. `npm install && npm run build` to verify it compiles.

## Write to manifest (`assembly`)
`repo_path="blueprint-out/app"`, `run_cmd="cd blueprint-out/app && npm run dev"`,
`wired=true`; `status.assembly="done"`.
