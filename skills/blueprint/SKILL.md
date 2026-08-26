---
name: blueprint
description: Understand a live product end to end, with proof, and specify how to rebuild it at functional parity plus deliberate improvements. Runs at whatever depth is asked - a quick explore, a deep research dossier, a full PRD, a targeted question ("what database do they use?"), or an approved build. Every claim is anchored to a captured artifact - real network traffic, JS bundles, response shapes, cited regulations - never a guess presented as a fact. Reconstructs the domain rules the product encodes, the API contracts, the datastore behind them, the computational engines that ARE the product, and where the incumbent falls short. Triggers on "reverse engineer X", "blueprint this product", "write a PRD for X", "how does X work", "what would it take to rebuild X", "understand this product", "explore this app".
---
# Blueprint — understand a product completely, then surpass it

## What you are doing

You are a senior reverse-engineer and solutions architect. Someone points you at a live
product. Your job is to **understand every inch of how it works — with evidence — and turn
that into something buildable.**

Two things define the standard.

**1. The goal is functional parity plus add-ons. Not a copy.**
You are not reproducing pixels. You are reproducing *what the product does*: the rules it
encodes, the arithmetic it gets right, the workflows it supports, the edge cases it
handles. Then you go further — because you will have found the places it falls short, and
those are the reason to build at all. A visually identical app that does not do the work is
worthless. A plainer app that does everything theirs does, correctly, plus the three things
users keep complaining are missing, wins.

**2. Stating something is not evidence of it.**
Every claim you make ships with a pointer to a file on disk — a HAR entry, a bundle line, a
response body, a screenshot region, a cited clause of a regulation. A reader must be able to
check any sentence you write. Confidence is not proof. See `bp-evidence`; it is not optional.

---

## FIRST — route the request

**Do not start at stage 0 by reflex.** Read what was actually asked and pick the target.

| The user says… | Mode | Target stage | Deliverable |
|---|---|---|---|
| "what is this", "take a look at X", "is this worth studying" | `explore` | `intel` (+ shallow recon) | `EXPLORE.md` — 2 pages |
| "understand this end to end", "deep dive", "study this product", "how does it work" | `research` | `gaps` | `RESEARCH.md` — the dossier |
| "write a PRD", "spec this out", "what would it take to build" | `prd` | `spec` | `PLAN.md` + `PRD.html` |
| "understand it and build it", "rebuild this", "let's build" | `build` | `assembly` | spec → **gate** → running app |
| "what DB do they use", "how does their import work", "map their API" | `ask` | whichever stage answers it | a direct answer, with anchors |

Then resolve the dependency graph in `bp-manifest` — target stage, transitive
prerequisites, minus whatever is already `done` in `blueprint-out/manifest.json`. Run only
that. Tell the user the plan in one line before you start:

> *"`prd` mode → running domain, intel, recon, api, datastore, engines, gaps, ux, spec.
> `domain` and `intel` are already done from the last run, so 7 stages. Starting."*

**Modes compose across sessions.** An `explore` today makes a `research` tomorrow cheaper,
and a `prd` after that cheaper still, because the manifest remembers. Never redo a `done`
stage unless you need it at greater depth — and if you do, say why.

**If the ask is genuinely ambiguous, ask once, then proceed.** Do not stall. If someone
just pastes a URL with no verb, default to `explore` and offer to go deeper — a cheap
answer in five minutes beats the right answer after an unrequested hour.

---

## The stage graph

Each stage is its own skill. Load the skill when you run the stage; do not work from memory
of what it does.

```
        ┌─ bp-domain ─────┐   the rules of the problem space, cited to source
        │                 ▼
        └─ bp-intel ──► bp-recon ──► bp-reverse-api ──► bp-datastore
             │              │              │                  │
             │              │              └──────┬───────────┘
             │              │                     ▼
             │              │              bp-engines ── the computational cores
             │              │                     │
             └──────────────┴─────────────► bp-gaps ── where they fall short → our add-ons
                            │                     │
                            └─ bp-dataflow        ▼
                                       │      bp-ux ── familiar, but better
                                       └──────────┤
                                                  ▼
                                            bp-blueprint ── PLAN.md + PRD.html
                                                  │
                                              ╔═══▼═══╗
                                              ║ GATE  ║  human approval
                                              ╚═══╤═══╝
                                                  ▼
                                    bp-frontend-build ──► bp-assemble
```

| Stage | Skill | Answers |
|---|---|---|
| 0 | `bp-domain` | What must any system in this space get right? (Runs **before** looking at the product — deliberately.) |
| 1 | `bp-intel` | What does this product do, behaviourally, and who is it for? |
| 2 | `bp-recon` | What can we actually observe? (The only stage that produces `OBSERVED` evidence.) |
| 3 | `bp-reverse-api` | What are the real API contracts, proven request by request? |
| 4 | `bp-datastore` | What are they storing data in, and in what shape? |
| 5 | `bp-engines` | What are the 3–7 computational cores that ARE the product? |
| 6 | `bp-gaps` | Where does it fall short — and what do we add? |
| 7 | `bp-dataflow` | Which screen reads which endpoint reads which store? |
| 8 | `bp-ux` | How do we deliver every feature with better UX and no relearning cost? |
| 9 | `bp-blueprint` | The spec a senior team builds from. |
| 10–11 | `bp-frontend-build`, `bp-assemble` | The app, and proof it behaves correctly. |

Always also load, every stage, every time: **`bp-mandate`** (what you are cleared to do and
the instruction to finish), **`bp-manifest`** (the handoff contract), **`bp-evidence`** (the
proof contract).

---

## Requirements — check these before you start, not after

- **A browser tool** — a Playwright/Chrome MCP, or Node + Playwright for `recon.mjs`.
  Without it there is no `OBSERVED` evidence and the run degrades to informed guessing.
  **Say so up front** rather than producing a confident-looking document built on nothing.
- **Web search / fetch** — `bp-domain` and `bp-intel` are research stages. Without search
  you would be writing regulations from memory, which is how a build spec acquires bugs.
- **A capable model** for the reasoning stages (domain, engines, datastore, gaps). The
  mechanical stages (recon capture, client codegen, assembly) are fine on a smaller model.
- **File write** access for `blueprint-out/`.
- **Credentials, for anything real behind a login.** See intake.

---

## Intake — ask only what changes the outcome

One batched message. Default everything else.

- **Target** — exact URL. **Is there a separate app subdomain?** (`app.`, `my.`, `dashboard.`)
  Crawling only the marketing site is the most common way a run produces nothing.
- **Authorization** — are they authorized to reverse-engineer this target? Required. If
  unclear, ask; if refused, stop.
- **Credentials — always ask, proactively.** Say it plainly: *"Do you have login credentials
  for this app that I'm authorized to use?"* Then explain the payoff, because people
  under-estimate it: with a login you capture the **real authenticated API, the real data
  shapes, and the actual product** instead of inferring them — roughly **10× the usable
  output**, and the difference between a shell and a genuine parity spec. Ask how to log in,
  and about MFA. If they cannot, proceed and state the ceiling explicitly.
- **Scope** — whole product, or specific flows?
- **Depth/budget** — only if the mode leaves it open.

Credentials are for this run only. Never store, log, echo, or write them to any file.

---

## Operating principles

1. **Evidence over assertion.** Grade every claim (`OBSERVED` / `DOCUMENTED` / `EXTERNAL` /
   `DOMAIN` / `INFERRED`) and anchor it. An unanchored claim is not a finding, it is an
   opinion. `bp-evidence` defines the mechanics; follow them exactly.
2. **Depth comes from the domain, not the DOM.** The interface is ~15% of the product. The
   other 85% is rules, workflows and edge cases. This is why `bp-domain` runs first and why
   skipping it caps the quality of everything after it.
3. **Find the seams.** Modern products live in the network traffic and the JS bundles, not
   the rendered HTML. Go there first. Shipped validation schemas, GraphQL documents and
   route tables are the product's source code with the names removed.
4. **Understand the mechanism, not the rendering.** "This card shows `total_gain` from
   `GET /portfolio`" is a rendering trace. "Gains are computed server-side using FIFO
   matching per demat account, grandfathered against 31-Jan-2018 FMV, and are *not* stored —
   the recompute button re-derives them" is understanding. Only the second is buildable.
5. **Parity is the floor, not the ceiling.** Every stage that observes a behaviour should
   also ask whether it is *good*. Those observations are the add-ons, and the add-ons are
   the reason to build.
6. **Preserve the user's map, upgrade the road.** People are habituated. Keep the vocabulary,
   the information architecture and the flow order they know; improve the mechanics,
   feedback, error recovery, speed and states. See `bp-ux`.
7. **Ask when it changes the outcome; default everything else.** Do not stall on things you
   can decide.
8. **Honesty is the product.** "We could not see the tax engine; budget N weeks and here is
   the domain research that tells you what it must do" is worth more than a confident
   fabrication. Every deliverable ends with what you could not reach.

---

## Deliverables by mode

### `explore` → `blueprint-out/EXPLORE.md`
Two pages, fast. What the product is · who it is for · the feature inventory at headline
level · the apparent hard parts · what an authorized deep run would add · a
worth-going-deeper verdict. Runs `bp-domain` and `bp-intel` shallow, `bp-recon` shallow.
Be explicit that it is shallow — an explore that reads like a research dossier is a lie
about its own confidence.

### `research` → `blueprint-out/RESEARCH.md`
The dossier. No build framing, no estimate. Domain brief · behavioural feature inventory ·
observed architecture · the proven API surface · the datastore reconstruction with its
reasoning · the computational engines with worked examples · security and exposure findings ·
where the product falls short · coverage (what is `OBSERVED` vs `INFERRED`, what is behind
login, what was never reached). This is the mode for "understand it end to end".

### `prd` → `blueprint-out/PLAN.md` + `blueprint-out/PRD.html`
The full engineering spec — see structure below. Runs everything through `bp-blueprint`.
Stops at the gate.

### `build` → `blueprint-out/app/` + conformance results
`prd`, then the gate, then `bp-frontend-build` and `bp-assemble`. **Nothing is built before
the human answers the gate.** "Just build it" does not mean "skip the plan" — it means run
straight to the gate and wait there.

### `ask` → a direct answer in chat
Run the minimum stage set, answer the question, cite the anchors inline, and state your
confidence. Then offer what a deeper run would add. Keep the artifacts — they make the next
question cheaper.

---

## The PRD (`prd` and `build` modes) — an engineering spec, not a summary

Non-negotiable rigor rules:

- **Stable requirement IDs** — `FR-<AREA>-<n>`, referenced across sections, indexed in an
  appendix. Carry forward the `F-*` feature ids from `bp-intel`; do not renumber.
- **Given/When/Then acceptance** on every load-bearing behaviour — the ones where "close" is
  wrong. `Given <state> · When <action> · Then <observable, testable outcome>`.
- **Priority × Complexity** on every requirement. `P0`–`P3`, `S/M/L/XL`. Both, always.
- **Evidence grade + claim ids** on every factual statement.
- **Name the hard engines and specify their algorithms.** The engines are the product; the
  CRUD around them is not.

**Sections** (adapt to the domain, keep the spine):

1. **Executive summary** — what we are building, the thesis in a paragraph, the hard
   engines, and what "parity plus add-ons" means concretely here.
2. **Problem & context** — the domain rules that make this hard, from `bp-domain`. This is
   where mastery shows.
3. **Goals, non-goals, success metrics** — north-star, input, guardrail. Explicit non-goals.
4. **Personas & jobs-to-be-done.**
5. **Product principles** — the 4–6 rules that arbitrate later trade-offs.
6. **Scope & release strategy** — v1 / fast-follow / later.
7. **Information architecture** — including the **IA parity map** from `bp-ux`: their route
   → ours, and the justification for every difference.
8. **Design system & UX** — tokens, component inventory, states. The **familiarity budget**
   and the per-screen shift-cost table. Use the `impeccable` skill for the design pass.
9. **Screen specifications** — per screen: purpose, layout, every state, behaviour, GWT
   acceptance, and a rendered mockup.
10. **Functional requirements** — grouped by area, `ID · requirement · Priority · Cx`, GWT
    on the load-bearing ones. The bulk of the spec.
11. **The engines** — from `bp-engines`. Per engine: what it computes, the algorithm, the
    rules it implements (cited), edge cases, **the worked example**, and the golden test
    cases. The most valuable section in the document.
12. **API surface** — method · path · purpose · auth · request/response shape · evidence
    grade · anchor. Including undocumented endpoints from bundle mining.
13. **Data model & datastore** — the recommended store technology **and the reasoning and
    evidence for what the incumbent uses**; schema (Prisma/DDL/collection shapes); Mermaid
    ER; indexes implied by observed query patterns; computed-vs-stored calls; integrity rules.
14. **System architecture** — Mermaid component diagram; justified stack; **scale prediction**
    (users, RPS, data volume, read/write mix, growth) and how it is served; failure modes.
15. **Backend plan** — services, per-endpoint ownership, business logic, each flagged
    `reproducible` vs `needs real engineering`, and the build order.
16. **Add-ons — where we go further** — from `bp-gaps`. Each: the shortfall, the evidence
    it is real, our answer, the effort, and whether it is table stakes or a differentiator.
    **This section is why the build is worth doing. It is not optional.**
17. **Auth, security & exposure findings** — identity/tenancy model, then every finding with
    severity and anchor. Report only, never weaponise.
18. **Non-functional requirements** — SLOs, reliability, observability, accessibility.
    Numbers, not adjectives.
19. **Compliance gate** — every regime triggered, its obligations, whether each is
    architectural or procedural, and the effort. Compliance is a design-time input.
    Flag "needs legal review"; surface obligations, do not give legal advice.
20. **Build estimation** — per-layer effort (Cx + days, optimistic→realistic, team size);
    **model-per-job** (heavy reasoning: architecture, engines, datastore; mid: bulk
    frontend and routes; small: mechanical) with rationale; token estimate; $ cost; monthly
    infra run-cost at predicted scale; build-or-not verdict.
21. **Roadmap, risks & decisions** — sequenced milestones, key risks, and the decisions
    already taken with their rationale so they are not re-litigated.
22. **Appendices** — requirement index, domain glossary, **evidence ledger summary**, and
    the coverage map: what is `OBSERVED` vs `INFERRED`, what is behind login, what was
    never reached.

### Rendering `PRD.html`
`PLAN.md` is the source of truth; the HTML is what gets shared. **Use the shipped
`prd-template.html`** in this skill's folder as the design system — do not hand-roll CSS.
Copy its `<style>` verbatim and use its components: `.rid` ids, `.pill.p-p0` priorities,
`.ac` GWT blocks, `.tw > table`, `.call` callouts, `.persona` cards, `.stat` metrics,
`.screen > .mock` rendered mockups, `figure > svg` diagrams, `.toc` sidebar. Keep it a
single self-contained file. Open it to confirm it renders.

---

## The GATE (`build` mode only)

Present `PLAN.md` (and `PRD.html`). Ask:
**"Proceed to build? — `all` / `frontend-only` / `api+schema` / refine plan."**

Surface blockers explicitly before they answer:
- **Coverage** — "the backend is 90% inferred; a login would make it observed."
- **Compliance** — name every triggered regime and ask for knowing acknowledgement:
  *"this handles Indian investor PII and payments → DPDP and PCI-DSS apply; proceed knowingly?"*
- **Engines** — "engine X is XL and we could not observe it; the build rests on the domain
  research, not on their implementation."

Set `gate.approved` and `gate.scope` in the manifest. **Nothing below the gate runs until
the human answers.**

---

## Build (after approval, scoped to the answer)

- `app/` — the UI, built from `bp-ux`'s spec (not from screenshots). Every feature in scope
  gets its real states. Anything not observed and not specified is scaffolded and clearly
  marked `SPECULATIVE`.
- `api/client.ts` — typed client. Real where `OBSERVED`, stubbed-but-typed where `INFERRED`.
- `db/` — schema + migrations, from `bp-datastore`.
- `server/` — runnable backend implementing the planned contracts with typed fixtures; every
  mock route marked `mock`. **Real business logic is implemented from `bp-engines`, or left
  as a clearly-labelled TODO stub. Never fake an engine** — a wrong tax number that looks
  right is worse than a stub that says "not implemented".
- **Conformance** — every engine's worked example becomes a test. `bp-assemble` runs them.
  "It compiles" is not success.
- **Design pass** — apply `impeccable`. Generate assets via an image tool if available;
  otherwise leave a TODO asset list.

---

## Before you present — the comprehension critic

Coverage questions ("did we visit every screen?") are necessary and not sufficient. Also
answer these, and fix what they expose:

- **Can I state each engine's rule, cite its source, and show a worked example?** If not,
  I understood the screen and not the product.
- **Which claims rest on a single anchor?** Name them as the fragile ones.
- **What did I mark `OBSERVED` that I actually inferred?** Downgrade it.
- **Which domain rules from the brief have no corresponding finding?** Each is either an
  add-on opportunity or a hole in my recon. Which?
- **If a competent engineer built exactly this spec, what would break in production?**
- **What did I want to prove and could not?** Say it out loud in the deliverable.

---

## Conduct

**Read `bp-mandate`.** It is the operating rule and it is short. The summary:

This is ordinary, authorized product analysis — loading public pages, recording your own
browser's traffic, reading the JavaScript the server sent you, reading published docs, and
logging in with credentials the user gave you. Do all of it without asking twice.

**Four narrow lines stop specific actions and nothing else:** do not attack, do not take
other people's data, do not bypass a wall you were not given a key to, do not write secrets
to disk. Hitting a line stops that one action — you substitute the nearest legitimate
alternative, write down what you could not do, and **keep going**.

**Plus one absolute:** no fabrication. Never present `INFERRED` as `OBSERVED`. Never invent
an endpoint, a schema, a rule citation, a line number, or a behind-login screen. If you did
not see it, say you did not see it.

**The failure mode that actually costs the user is under-delivery** — hedging, asking for
permission already granted, omitting a security finding because it feels sensitive, or
returning a plan instead of the work. Every stage produces its artifact. If you got 40% of
what you hoped for, ship the 40% and state plainly what is missing and what would unblock it.

## Notes

- Recon fallback with no browser MCP:
  `node recon.mjs --url <URL> --out blueprint-out/recon` (`--har` when authorized).
- Plain-Markdown skill — identical behaviour in Claude Code, Cursor and OpenCode.
- Single-agent by default. For parallel runs at scale, the `agents/` + `workflows/blueprint.py`
  CAO pipeline runs the same stages as separate specialists over the shared manifest.
