---
name: bp-blueprint
description: Master synthesis. Reads recon output (screenshots + DOM) for a target and produces ONE blueprint.md — full clone strategy, per-stage plan, and the agent/model responsible for each stage.
---
# bp-blueprint — the master document

Input: `run/blueprint-out/recon/` (screenshots, DOM, recon.json) for a target URL.
Output: `run/blueprint-out/blueprint.md` — the single deliverable a builder reads to
clone the product. Read the screenshots (vision) and DOM, then write the doc with
EXACTLY these sections:

1. **Overview** — what the product is, who it's for, the core value (1 paragraph).
2. **Feature map** — every feature observed, grouped (public site vs. gated app).
   Mark anything behind login as `[inferred — behind auth]`.
3. **Tech stack (observed)** — frameworks/libs detected from DOM, headers, asset
   names, meta tags. State evidence; don't guess blindly.
4. **Data model** — inferred tables/entities + key fields, from the UI. Prisma block.
5. **API surface** — likely endpoints per feature (REST paths + method + purpose),
   marked `observed`/`inferred`.
6. **Dataflow map** — table: UI element → data fields → API endpoint → DB table(s).
7. **Clone implementation plan** — ordered, concrete build steps to reproduce it.
8. **Stage → agent → model matrix** — the table below, filled for THIS target.
9. **Risks & gaps** — what recon couldn't see (auth-gated app, subdomains), and what
   an authorized run would add.

## Stage → agent → model matrix (fill per target)
| Stage | Agent | Tool reused | Model (default) |
|---|---|---|---|
| 0 recon | recon-agent | Playwright (recon.mjs) | none (mechanical) |
| 1 intel | intel-agent | saas-reverse | Claude Opus (vision+reasoning) |
| 2 database | db-agent | native Claude vision | Claude Opus |
| 3 api | api-agent | reverse-api-engineer / Integuru | Claude Opus (+ Sonnet for codegen) |
| 4 dataflow | dataflow-agent | — (fusion) | Claude Opus |
| 5 frontend | frontend-agent | ai-website-cloner-template | Opus planner + Sonnet section builders |
| 6 assemble | assembler-agent | — (glue) | Claude Sonnet |

Keep it evidence-led: every claim is either `observed` (seen in a shot/DOM) or
`inferred` (reasoned). Also update `run/blueprint-out/manifest.json` slices as you go.
