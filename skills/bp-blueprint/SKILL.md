---
name: bp-blueprint
description: Stage 9 — synthesis. Fuses every prior stage into the single deliverable for the requested mode - EXPLORE.md, RESEARCH.md, or PLAN.md plus a rendered PRD.html. Runs the comprehension critic before publishing, and reports coverage honestly. This stage writes nothing new; if a fact is not in an upstream artifact or the evidence ledger, it does not appear.
---
# bp-blueprint — write the deliverable

## Your job

Everything is gathered. Turn it into **one document a senior team can act on**.

The hard discipline here: **you are a synthesiser, not an author.** Every fact comes from an
upstream artifact and carries its claim id. If you find yourself writing a sentence you
cannot trace to the ledger, you are inventing — stop and either go get the evidence or cut
the sentence.

Your value-add is structure, sequencing, judgement about what matters, and honesty about
what is missing. Not new facts.

## Load first

- **`bp-mandate`**, `bp-manifest`, `bp-evidence`
- **Every produced artifact.** Read them; do not summarise from the manifest's index fields.
- `blueprint-out/evidence/ledger.jsonl` — the full claim set
- `prd-template.html` from the `blueprint` skill folder, for `PRD.html`
- The requested **mode** — it decides which document you write

---

## Pick the document

| Mode | Write | Length | Rule |
|---|---|---|---|
| `explore` | `EXPLORE.md` | ~2 pages | Fast read. Say plainly that it is shallow. |
| `research` | `RESEARCH.md` | as long as the evidence supports | Understanding, no build framing, no estimate |
| `prd` / `build` | `PLAN.md` + `PRD.html` | full spec | The 22-section structure in the `blueprint` skill |
| `ask` | answer in chat | short | Answer, anchors inline, confidence, then offer depth |

---

## Method

### 1. Check what you actually have

Read `status` for every stage. Note what ran, at what depth, and what did not.

**A missing stage is a hole you declare, never one you fill.** If `engines` never ran, the
document does not contain an engines section written from your imagination — it contains a
line saying the engines were not analysed and what that costs the reader. This is the single
most important rule of this stage.

### 2. Assemble in dependency order

Build the document from the artifacts, in the order the reader needs them: problem and
domain → what the product does → how it works → where it falls short → what we build →
what it costs. Each section pulls from its stage.

Carry ids forward. `F-*` features become `FR-*` requirements. `GAP-*` becomes add-on
requirements. `ENG-*` becomes the engines section and the conformance suite. `DOM-*`
citations travel with their rules. **Never renumber.** A reader tracing `FR-IMP-021` back to
`GAP-07` back to `DOM-047` is the whole point of the id discipline.

### 3. Write the sections that only exist here

Most sections are assembly. Three require real synthesis:

- **Executive summary** — the thesis in a paragraph. What this product is, what makes it
  hard, what we would build, why it wins. Write it last, when you know the answer.
- **Build estimation** — pull effort from every stage (`engines` sizes the hard part,
  `ux` the screen count, `api` the surface, `datastore` the schema, `gaps` the add-ons).
  Add integration, testing, infrastructure and the reference-data pipelines the engines
  need. Give optimistic → realistic with team size. Then model-per-job, token estimate,
  $ cost, and monthly run-cost at the predicted scale. End with a **build-or-not verdict**
  and say it plainly.
- **Coverage** — what is `OBSERVED` vs `INFERRED`, with counts from the ledger. What is
  behind login. What was never reached. Which claims rest on a single anchor. **This is the
  section that makes the rest trustworthy.** Never soften it.

### 4. Run the comprehension critic — before publishing, not after

Coverage checks ask "did we look everywhere". These ask "did we understand it". Answer each
in writing, fix what they expose, and re-run:

1. **Can I state each engine's rule, cite its source, and show a worked example that
   arithmetically checks out?** If not, we understood the screens, not the product. Go back.
2. **Does every claim graded `OBSERVED` have an anchor that resolves to a file that exists?**
   Run the `bp-evidence` self-check. Fix or downgrade every failure.
3. **Which load-bearing claims rest on a single anchor?** List them in coverage as fragile.
4. **Which domain rules have no corresponding finding?** Each is either an add-on or a hole
   in recon. Decide which, for each one. Do not leave them unresolved.
5. **Does every feature in the inventory appear in the requirements?** Parity is functional;
   an unmapped feature is a parity failure and must be listed as one.
6. **Would a competent team building exactly this spec ship something correct?** Where the
   honest answer is no, name the gap in the spec, not in the team.
7. **What did I want to prove and could not?** Say it in the document.

### 5. Render `PRD.html` (prd / build modes)

`PLAN.md` is the source of truth. The HTML is what gets shared with founders and executives.

**Use `prd-template.html` as the design system — do not hand-roll CSS.** Copy its `<style>`
block verbatim. Use its components: `.rid` requirement ids, `.pill.p-p0` priority pills,
`.ac` Given/When/Then blocks, `.tw > table` requirement tables, `.call` callouts
(decision/risk/note/sec), `.persona` cards, `.stat` metric cards, `.screen > .mock` rendered
mockups (take these from `blueprint-out/ux/mocks/`), `figure > svg` for diagrams, and the
`.toc` sidebar with numbered sections.

Keep it a single self-contained file. Open it and confirm it renders before you finish.

### 6. Present

Summarise in chat: what was found, the three things that matter most, the verdict, and the
top gaps. Then, for `build` mode only, put the gate question.

---

## Emit

Per mode, plus always:

- `blueprint-out/evidence/summary.md` — ledger statistics: claims by grade, by stage,
  fragile claims, unresolved contradictions
- Manifest slice `spec`:

```jsonc
"spec": {
  "mode":"prd","plan":"blueprint-out/PLAN.md","prd_html":"blueprint-out/PRD.html",
  "requirements":{"total":214,"p0":63},
  "coverage":{"observed":389,"documented":142,"external":88,"domain":47,"inferred":203,
              "behind_login":12,"never_reached":4,"single_anchor_claims":18},
  "feature_parity":{"total":47,"specified":47,"unmapped":[]},
  "critic":{"run":true,"issues_found":9,"issues_fixed":9},
  "estimate":{"optimistic_days":112,"realistic_days":186,"team":4,
              "token_estimate":"14M","usd_estimate":"~$430","monthly_infra":"$1,900"},
  "verdict":"build — clear wedge on correctness + import reliability"
}
```
Then `status.spec = "done"`.

---

## Done when

- [ ] The document matches the requested mode
- [ ] Every section traces to upstream artifacts; nothing invented
- [ ] Ids carried forward unchanged and cross-referenced
- [ ] Missing stages declared as gaps, never filled in from imagination
- [ ] Comprehension critic run, all seven questions answered in writing, issues fixed
- [ ] `bp-evidence` self-check passes — every `OBSERVED` anchor resolves
- [ ] Coverage section complete and honest, with counts
- [ ] Every feature mapped to requirements, or listed as unmapped with a reason
- [ ] Estimate includes engines, reference data, integration, testing and infrastructure
- [ ] Verdict stated plainly
- [ ] `PRD.html` renders (prd/build modes)

---

## Never

- Never write a section for a stage that did not run.
- Never state a fact without a traceable claim id.
- Never renumber ids from upstream stages.
- Never soften the coverage section. It is what makes the document credible.
- Never present the estimate without the engines' contribution — that is where estimates
  break, and an estimate that omits it is worse than no estimate.
- Never publish before the critic. Finding a fabricated anchor yourself is cheap; the reader
  finding it costs you the whole document.
