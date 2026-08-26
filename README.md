# Blueprint — understand a product completely, then surpass it

Point it at a live product. It works out **how the thing actually works** — the domain rules
it encodes, its real API contracts, the database behind them, the computational engines that
*are* the product — and turns that into something buildable.

Two things define it:

**The goal is functional parity plus add-ons, not a copy.** Not pixels — what the product
*does*: the rules, the arithmetic, the workflows, the edge cases. Then further, because the
run finds where the incumbent falls short and that is the reason to build at all.

**Every claim carries its proof.** Each finding is anchored to a file on disk — a HAR entry,
a JS bundle line, a response body, a cited clause of a regulation. Nothing is asserted
without a pointer you can check. `INFERRED` is never dressed up as `OBSERVED`.

## Modes — it runs at whatever depth you ask for

| You say | Mode | You get |
|---|---|---|
| "take a look at X" | `explore` | 2-page read, ~15 min |
| "understand this end to end" | `research` | `RESEARCH.md` — the full dossier |
| "write a PRD for X" | `prd` | `PLAN.md` + a shareable `PRD.html` |
| "understand it and build it" | `build` | spec → **your approval** → running app |
| "what database do they use?" | `ask` | a direct answer with anchors |

Stages form a dependency graph, not a fixed pipeline. Modes compose across sessions — an
`explore` today makes tomorrow's `prd` cheaper, because the manifest remembers what is done.

## Install

### Claude Code
```
/plugin marketplace add <your-org>/blueprint
/plugin install blueprint@blueprint-marketplace
```

### Cursor / OpenCode
```bash
npx github:<your-org>/blueprint install
```

## Use

```
/blueprint https://example.com
/blueprint write a PRD for https://example.com
/blueprint what database does https://example.com use?
```

Or just describe what you want. Everything lands in `blueprint-out/`.

## Requirements

- **A browser tool** — a Playwright/Chrome MCP, or Node + Playwright for the bundled
  `recon.mjs`. Without it there is no observed evidence. **The #1 gotcha.**
- **Web search** — the domain and intel stages are research, not crawling.
- **A capable model** for the reasoning stages. Mechanical stages run fine on a small one.
- **Login credentials** for the target, if you want the real backend. This is the single
  biggest quality lever in the whole system — it turns an inferred API into an observed
  contract, roughly 10× the usable output.

## The stages

```
domain ─┐                     the rules of the problem space, cited to source
intel ──┴──► recon ──► api ──► datastore        what it does · what we can see
                        └──► engines            the computational cores that ARE the product
                        └──► gaps               where they fall short → our add-ons
                        └──► dataflow           the wiring map
                             └──► ux            familiar to use, better to use
                                  └──► spec ──► ║ GATE ║ ──► frontend ──► assembly
```

- **`domain` runs before anyone opens the product.** Deliberately. Start from the screens and
  you only ever see what the screens show — roughly 15% of the product.
- **`engines` is the one that matters.** Per engine: the algorithm, the cited rules, the edge
  cases, and a worked example with real numbers. That is what makes the spec buildable.
- **`gaps` is why you'd build.** Parity is not a business case; the add-ons are.
- **`assembly` reports conformance, not compilation.** Golden test vectors from `engines` run
  against the build. A repo that typechecks with every rule stubbed is a demo, and it says so.

## Honesty

Claims are graded `OBSERVED` / `DOCUMENTED` / `EXTERNAL` / `DOMAIN` / `INFERRED`, and every
one is registered in `blueprint-out/evidence/ledger.jsonl` with a resolvable anchor. The
coverage section states what is inferred, what is behind login, and what was never reached.

Engines are implemented from spec or stubbed with a throwing `NotImplementedError` — **never
a plausible wrong number**, because someone will act on it.

## Conduct

This is ordinary, authorized product analysis: public pages, your own browser's traffic, the
JavaScript the server sent you, published docs, and a login you were given. Four narrow lines
stop specific actions — don't attack, don't take other people's data, don't bypass a wall,
don't write secrets to disk. Hitting one stops that action, never the run.

`skills/bp-mandate/SKILL.md` states it plainly, because the failure that actually costs you
is an agent that hedges and delivers nothing.

## Layout

| Path | What |
|---|---|
| `skills/blueprint/` | The entry skill — mode router, intake, PRD structure |
| `skills/bp-mandate/`, `bp-manifest/`, `bp-evidence/` | Contracts every stage loads |
| `skills/bp-*/` | One skill per stage |
| `agents/` | Specialist definitions for the CAO multi-agent path |
| `commands/blueprint.md` | The `/blueprint` slash command |
| `workflows/blueprint.py` | Durable CAO workflow — same stages, resumable, parallel |
| `plugin/`, `.claude-plugin/` | Claude Code plugin packaging |
| `bin/install.js` | Cross-platform `npx` installer |

## License

MIT
