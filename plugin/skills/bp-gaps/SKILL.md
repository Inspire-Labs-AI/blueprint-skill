---
name: bp-gaps
description: Stage 6 — find where the incumbent falls short and turn it into our add-on list. Mines reviews, support threads, forums, changelogs, incident history and the observed product itself for real, evidenced shortfalls, then specifies what we build instead. This is the stage that makes the rebuild worth doing; without it the plan can only ever reach parity.
---
# bp-gaps — where they fall short, and what we do about it

## Your job

Everything up to now described what the product **does**. This stage asks whether it does it
**well**, and turns the answer into a build list.

This is the stage that justifies the project. Parity alone is not a business case — nobody
switches to an identical product. **The add-ons are the reason to build.** Your output is
the section a founder reads to decide yes or no.

Two rules keep this honest:

1. **Every gap needs evidence.** "Their UI feels dated" is an opinion. "Fourteen reviews
   across G2 and Reddit in the last eight months describe the import as failing silently on
   password-protected PDFs [GAP-012..GAP-025], and we confirmed the error state gives no
   recovery path [GAP-026]" is a finding.
2. **Every gap needs an answer.** A complaint list is not a deliverable. Each gap ships with
   what we build instead, what it costs, and whether it is table stakes or a differentiator.

## Scope — do only this

- **Deliver:** the ranked add-on list — each gap evidenced, each with what we build instead,
  its effort, and table-stakes vs differentiator.
- **Do not:** design the add-on's screens (that is `ux`) or spec its algorithm (that is
  `engines`). You name the shortfall and the answer at requirement level; you do not build it
  here. A gap with a complaint but no answer, or an answer with no evidence, is not a finding.
- **Emit:** the files under `## Emit`, the `gaps` slice, and `GAP-*` ledger lines.
- **Stop when:** every gap has both evidence and an answer, and the wedge (or its absence) is
  stated. A complaint list is not this stage's output.

## Load first

- **`bp-mandate`** — read it first. Reading public reviews and forum posts is ordinary
  market research. Criticising a product's engineering from evidence is analysis, not
  disparagement. Be direct.
- `bp-manifest`, `bp-evidence` (your prefix is `GAP`)
- `blueprint-out/intel/features.md` + `positioning.md` + `reconciliation.md`
- `blueprint-out/domain/domain-brief.md` — **the domain rules are the yardstick.** A rule
  the product does not implement is the highest-value gap there is.
- `blueprint-out/recon/coverage.md` — the ❌ hunt-list items are pre-found gaps
- `blueprint-out/engines/verification.md` — **any spec-vs-observed mismatch traced to their
  error is a correctness gap, and correctness is the most defensible add-on that exists**
- `blueprint-out/api/` — response times, error handling quality, missing bulk operations

---

## Method — six sources, run all of them

### 1. What users actually say

Read, in this order of value:

- **3-star reviews** on G2, Capterra, TrustRadius. Not the 5s (marketing) or the 1s (usually
  billing disputes). **Three-star reviewers describe specific limitations precisely** — they
  like the product and are telling you exactly what is wrong with it.
- **Support forum threads**, especially unanswered ones and ones closed without resolution.
- **Reddit and HN**: search `"<product>" frustrating|annoying|workaround|switched|instead of`
  and `"<product>" vs`. Comparison threads are dense with specifics.
- **App / Play store reviews** if mobile exists — sorted by most recent, not most helpful.
- **The vendor's own feature-request board** if public. Vote counts are a ranked backlog
  handed to you.
- **Churn signals**: "we moved from X to Y because…" posts are the single most valuable
  source in this section. Search for them specifically.

For each complaint: what breaks, how often it is mentioned, over what period, whether the
vendor responded, and whether it is still true in the current product (check against recon).

**A complaint the vendor already fixed is not a gap.** Verify before you list it.

### 2. What the changelog admits

Read 12–24 months of release notes:
- **Repeated fixes to the same area** = a structurally fragile subsystem. They will keep
  fixing it; we can design it right once.
- **Long-requested features that never shipped** = architecturally hard for them, or not a
  priority. Either is an opening.
- **Removed features** = something did not work. Find out what.
- **Long silences** in an area = unmaintained.

### 3. What the incident history admits

The status page archive names which subsystems fail and how often. Repeated incidents in one
component is a reliability gap you can design around — and an SLO you can promise that they
cannot.

### 4. What the domain says they are missing

**This is the highest-value source and only you have it.** Walk `domain-brief.md` rule by
rule, edge case by edge case, and check each against `features.md` and `coverage.md`:

- **A domain rule with no implementation** → they handle it manually, wrongly, or not at all.
  Verify which. If a regulated computation ignores a rule, that is not a feature gap, it is a
  correctness defect, and it is the strongest possible reason to build.
- **A practitioner edge case with no handling** → the "we hit this every quarter and have to
  do it in Excel" gap. These are what make professionals switch.
- **A required output artifact they do not produce** → a filing format, an export, a
  reconciliation report.
- **A data source they do not support** → an unsupported broker, format or integration is a
  hard blocker for that whole segment of users.

### 5. What you observed yourself

From recon, judged directly and specifically:

- **Missing states** — no empty state, no loading feedback, errors with no recovery path.
- **Workflow friction** — count the clicks and page loads for a core task. If the domain
  workflow implies bulk operations and the UI is one-at-a-time, that is a gap with a number
  attached.
- **Latency** — from the HAR. Which endpoints are slow, and are they on the critical path?
- **Error quality** — does a failed import say which row failed and why, or just "error"?
- **No bulk / no API / no export** — professionals need all three. Check.
- **Mobile and accessibility** — if the domain has field or on-the-go usage and mobile is
  broken, that is a segment they cannot serve.

Be specific and quantified. "Slow" is not a finding; "the holdings list takes 4.2s at 500
rows [anchor], and the domain's professional persona routinely holds 5,000" is.

### 6. Structural and strategic gaps

- **Segments they cannot serve** — from pricing and entitlements. Who is priced out, gated
  out, or unsupported?
- **Pricing model mismatch** — per-seat pricing on a product used by one person per firm;
  usage pricing on a workload with a seasonal peak.
- **Architectural ceilings** — from `bp-datastore`. If their store cannot do multi-entity
  transactions and the domain needs them, that ceiling is permanent for them.
- **Trust and compliance gaps** — from the domain brief's compliance table. A missing
  certification blocks an entire buyer segment.

---

## Turning gaps into add-ons

Every gap becomes a row. **A gap without an answer does not ship.**

```markdown
### GAP-07 · Import fails silently on password-protected contract notes

- **Shortfall** — password-protected broker PDFs fail with a generic "could not parse"
  and no prompt for a password.
- **Evidence** — 9 review/forum mentions over 14 months [GAP-031..GAP-039]; reproduced in
  recon, error body carries no error code [GAP-040]; domain brief flags this format as
  standard for 3 of the 5 major brokers [DOM-047].
- **Who it hurts** — every user of those brokers. From the domain's persona work, the
  professional segment hits it every filing cycle.
- **Severity** — high · **Frequency** — common · **Still true** — yes, verified 2026-08
- **Our answer** — detect encryption on upload, prompt for the password inline, retry, and
  cache the password for the session. Per-row error reporting with a resolve-and-continue
  review step rather than an all-or-nothing failure.
- **Requirement** — `FR-IMP-021`
- **Effort** — M (~4 days)
- **Type** — **table stakes** (they should already do this) vs **differentiator**
- **Defensibility** — low: they could copy it in a sprint. Compare with GAP-02
  (correctness), which requires them to rebuild their engine.
```

Then rank. Sort by `(user pain × frequency × segment size) ÷ effort`, and separate:

- **Table stakes** — must exist for us to be a credible alternative. Not differentiators;
  the cost of entry. Be honest about which is which — most "add-ons" are table stakes.
- **Differentiators** — the reason someone switches. Aim for **three**, well chosen, not
  twenty. A long list of small improvements does not move anyone.
- **Structural advantages** — things they cannot easily copy because of an architectural,
  pricing or business-model constraint. Rare, and worth more than everything else combined.

Then write **the wedge**: one paragraph naming the segment we win first and the two or three
things that win it. If you cannot write that paragraph convincingly, say so — "there is no
clear wedge, this is a parity play in a crowded market" is a legitimate and valuable finding,
and the founder needs to hear it before spending a year.

---

## Proof requirements

- Every gap cites its sources: review URLs + quotes, forum links, changelog entries, or an
  `OBSERVED` anchor from recon. **Three independent mentions before you call something a
  pattern** — one angry reviewer is noise.
- Every gap is verified as **still true** against the current product, or explicitly marked
  "historical — appears fixed".
- Severity and frequency are your judgement, marked `INFERRED`, with the reasoning shown.
- Effort estimates are rough and labelled as such.
- **Correctness gaps from `bp-engines` carry the engine's evidence** — those are the ones
  that matter most, so they need the tightest sourcing.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/gaps/gaps.md` | Every gap, specified as above |
| `blueprint-out/gaps/addons.md` | The ranked add-on list, split into table stakes / differentiators / structural |
| `blueprint-out/gaps/wedge.md` | The one-paragraph positioning conclusion |
| `blueprint-out/evidence/ledger.jsonl` | Append `GAP-*` |

Manifest slice `gaps`:
```jsonc
"gaps": {
  "doc":"blueprint-out/gaps/gaps.md","addons":"blueprint-out/gaps/addons.md",
  "gaps":[{"id":"GAP-07","title":"...","severity":"high","frequency":"common",
           "type":"table-stakes","still_true":true,"effort":"M",
           "requirement":"FR-IMP-021","sources":["GAP-031","GAP-040","DOM-047"]}],
  "counts":{"total":23,"table_stakes":14,"differentiators":6,"structural":3},
  "correctness_gaps":[{"id":"GAP-02","engine":"ENG-01","note":"proceeds cap not applied","claim":"ENG-044"}],
  "wedge":"...",
  "verdict":"clear wedge | parity play | no clear opening"
}
```
Then `status.gaps = "done"`.

---

## Done when

- [ ] All six sources worked, not just reviews
- [ ] 3-star reviews read specifically
- [ ] Churn posts ("we switched from X to Y because…") searched for
- [ ] Changelog read for repeated-fix patterns
- [ ] **Domain brief walked rule by rule against the feature inventory**
- [ ] Engine correctness mismatches incorporated
- [ ] Every gap verified as still true
- [ ] Every gap has an answer, an effort, and a requirement id
- [ ] Ranked, and split into table stakes / differentiators / structural
- [ ] The wedge written — or its absence stated plainly
- [ ] Ledger self-check passes

---

## Never

- Never list a gap without evidence. Taste is not a finding.
- Never list a gap without an answer. This is a build list, not a review.
- Never call something a differentiator when it is table stakes. Founders build on this
  distinction, and getting it wrong costs them a year.
- Never inflate the count. Six real, evidenced gaps beat thirty speculative ones, and the
  thirty destroy the credibility of the six.
- Never skip the domain walk because the reviews were productive. The domain gaps are the
  ones no competitor reading the same reviews will find.
- Never manufacture a wedge that is not there. "This is a crowded parity play" is a finding
  the user needs, and delivering it honestly is the job.
