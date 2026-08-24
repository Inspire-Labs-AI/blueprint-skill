# Blueprint — plan-first web-app cloner

Give it a URL. It crawls the live product, **captures the real network APIs** (not guesses),
and produces a plan + system design + effort/token/$ estimate — then **stops for your
go-ahead** before building the clone (frontend + typed API client + schema + mock backend +
design pass). Runs natively in **Claude Code, Cursor, and OpenCode**. No Docker required.

## Install

### Claude Code (no npm, straight from GitHub)
```
/plugin marketplace add <your-org>/blueprint
/plugin install blueprint@blueprint-marketplace
```

### Cursor / OpenCode (or all three at once)
```bash
npx github:<your-org>/blueprint install
```
Installs the `blueprint` skill + `/blueprint` command into every platform found.

## Requirements
Before running, the agent needs:
- **A browser tool** — a Playwright/Chrome MCP (or Node + Playwright for the `recon.mjs` fallback).
  This is what captures real screens + network APIs; without it, results are guesswork. **#1 gotcha.**
- **A capable model** — Opus/Sonnet-class. It's an autonomous multi-stage operator.
- **File write** access (for `blueprint-out/`).
- **Login credentials** for the target (authorized) if you want the *real* backend, not an inferred one.

## Use
```
/blueprint https://example.com
```
or just say *"clone this site"*. It writes everything into `blueprint-out/` in your repo:
`PLAN.md`, screenshots, `db/schema.prisma`, `api/client.ts`, and (after approval) the app.

**Phase 1** → recon + real API capture + `PLAN.md` (features, API surface, data model,
system design, coverage, security, estimate). **Gate** → you approve (`all` /
`frontend-only` / `authorized`). **Phase 2** → build the scoped clone.

## Honesty
Every claim is tagged **observed** (seen in browser/network) or **inferred** (reasoned).
It never presents a behind-login page or an un-captured backend as if it were real. The
single biggest quality lever is an **authorized login capture** — it turns the inferred
backend into an observed API contract.

## What's in here
- `plugin/`, `.claude-plugin/` — Claude plugin marketplace (install with no npm)
- `skills/blueprint/`, `commands/blueprint.md` — the skill + slash command
- `bin/install.js`, `package.json` — the `npx` cross-platform installer
- `skills/bp-*`, `agents/`, Docker files — optional CAO pipeline for running stages in
  parallel / at scale (the "agentize + offer as a service" path)
- `BLUEPRINT-REPORT.md` — an example full report

## License
MIT
