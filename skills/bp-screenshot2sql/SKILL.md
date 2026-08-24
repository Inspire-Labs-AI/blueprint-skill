---
name: bp-screenshot2sql
description: Stage 2 DB. Infers DB schema (Prisma + SQL + tables) directly from UI screenshots using Claude's own vision — no external API, no OpenRouter.
---
# bp-screenshot2sql — native Claude vision, no third-party key

The tool this used to wrap (`screenshot2sql`) is just a vision-LLM that reads a UI
and writes a schema. Claude Code already does that — so we do it in-house. No
OpenRouter, no pip install, no key beyond the Claude Code you're already running.

## Method
1. Read every `recon.screenshots` image (Claude reads PNGs directly).
2. For each screen, list the entities and fields the UI implies (a table of orders →
   `orders(id, customer, amount, status, created_at)`; a settings form → its columns).
3. Merge/dedupe entities across all screens into ONE normalized schema. Infer keys,
   foreign keys, and types from labels + relationships shown in the UI.
4. Emit:
   - `blueprint-out/db/schema.prisma`
   - `blueprint-out/db/schema.sql`  (CREATE TABLE)
   - `blueprint-out/db/er.mmd`      (Mermaid ER diagram)

## Write to manifest (`database`)
`schema_prisma`, `schema_sql`, `er_diagram`, `tables`; `status.database="done"`.
Everything here is UI-inferred → each table is `confidence: "inferred"` unless a real
DB was authorized.

> Optional, authorized only: `dba-mcp` `replicate_database` to clone a real DB.
> Optional, if you'd rather not reason it by hand: the `screenshot2sql` CLI still
> works, but it needs OPENROUTER_API_KEY — skip it, Claude covers this for free.
