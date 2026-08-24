---
name: bp-cloner-template
description: Stage 5 frontend. Reuses ai-website-cloner-template's /clone-website flow (parallel per-section builder agents in worktrees) to build a Next.js clone.
---
# bp-cloner-template — reuse

Wraps `JCodesMore/ai-website-cloner-template` (agent template, Claude Code native).

## Get it
```bash
git clone https://github.com/JCodesMore/ai-website-cloner-template vendor/cloner-template
```

## Run
From that template's workspace, invoke its native flow:
```
/clone-website $TARGET_URL   # + any target.extra_urls, space-separated
```
Feed it `recon.screenshots` for pixel fidelity and `dataflow.map` so each section is
generated already knowing the data fields it must render (wire to the Stage-3 client,
not mock data, where `dataflow` gives an endpoint).

Output: Next.js 16 + shadcn + Tailwind v4 repo → move to `blueprint-out/frontend/`.

## Write to manifest (`frontend`)
`repo_path`, `framework`, `sections`, `routes`; `status.frontend="done"`.

> Fallback: if the template flow is unavailable, `npx morph clone $TARGET_URL` gives
> a fast single-pass Next.js codebase instead.
