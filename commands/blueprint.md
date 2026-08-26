---
description: Understand a product end to end with proof, then specify how to rebuild it at functional parity plus add-ons. Modes — explore, research, prd, build, ask.
---
Run the **blueprint** skill on: $ARGUMENTS

Load `skills/blueprint/SKILL.md` and follow it. Also load `bp-mandate`, `bp-manifest` and
`bp-evidence` — every stage needs all three.

**First, route the request.** Do not start at stage 0 by reflex. Read what was asked:

| The ask contains | Mode | Deliverable |
|---|---|---|
| "explore", "take a look", "what is this", or just a bare URL | `explore` | `EXPLORE.md`, ~2 pages |
| "understand", "deep dive", "research", "study", "how does it work" | `research` | `RESEARCH.md` dossier |
| "prd", "spec", "what would it take", "how hard" | `prd` | `PLAN.md` + `PRD.html` |
| "build", "rebuild", "understand it and build it" | `build` | spec → **gate** → running app |
| a specific question ("what DB", "map their API", "how does import work") | `ask` | direct answer with anchors |

Then resolve the stage dependency graph from `bp-manifest`: target stage → transitive
prerequisites → minus anything already `done` in `blueprint-out/manifest.json`. Run only
that, and say in one line what you are about to run before you start.

**Ask the intake questions once, batched:** the exact URL (**and whether there is a separate
app subdomain** — `app.`, `my.`, `dashboard.`), authorization, **credentials** (ask
proactively; a login turns an inferred backend into an observed contract — roughly 10× the
usable output), and scope. Default everything else. If no URL was given, ask for one.

**The standard:**

- Every claim carries an evidence grade and an anchor to a file on disk. Stating something is
  not proof of it.
- Tag `OBSERVED` (seen in browser/network/bundle) · `DOCUMENTED` (vendor's own words) ·
  `EXTERNAL` (third party) · `DOMAIN` (cited rule) · `INFERRED` (reasoned, with its basis).
  **Never present `INFERRED` as `OBSERVED`.**
- Capture the real network traffic. Do not infer what you can observe.
- The goal is **functional parity plus add-ons**, not a copy. Reproduce what it *does* — the
  rules, the arithmetic, the edge cases — then improve on it where the evidence shows it
  falls short.
- Preserve the user's vocabulary, navigation and flow order. Improve the mechanics.

**For `build` mode: STOP at the gate.** Present the plan and wait for `all` /
`frontend-only` / `api+schema` / refine. Write no application code before the human answers.
"Just build it" means run straight to the gate, not skip it.

**Deliver.** If a stage gets 40% of what it hoped for, it ships the 40% and says plainly what
is missing and what would unblock it. An empty output with an explanation of why the task was
hard is the one outcome this pipeline treats as failure — see `bp-mandate`.
