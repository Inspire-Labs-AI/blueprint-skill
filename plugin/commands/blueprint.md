---
description: Plan-first web-app cloner — crawl, capture real APIs, plan + estimate, gate, then build.
---
Run the **blueprint** skill on this target: $ARGUMENTS

Follow the blueprint skill exactly — do NOT skip the network capture, do NOT fabricate anything:

1. **PHASE 1 — recon + plan.** Crawl every reachable screen with the Playwright MCP;
   CAPTURE the real network API calls (method, URL, payload, response, auth) — do not
   infer what you can observe. Then write `blueprint-out/PLAN.md`: overview, screen
   inventory, discovered API surface, data model, coverage %, security/compliance, and a
   time + token/$ estimate with a build-or-not recommendation.
2. **STOP.** Show me PLAN.md. Do NOT write any clone code until I reply with one of:
   `all` · `frontend-only` · `authorized` (I provide login so you capture the REAL API).
3. **PHASE 2 — build** the approved scope into `blueprint-out/` (app/, api/client.ts, db/schema.prisma).

Tag every claim **observed** (seen in browser/network) or **inferred** (reasoned).
Never present a behind-login page or inferred API as if it were real.
If no URL was provided in $ARGUMENTS, ask me for one.
