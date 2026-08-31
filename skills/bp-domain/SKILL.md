---
name: bp-domain
description: Stage 0 — become an expert in the PROBLEM before looking at the product. Researches the rules, regulations, workflows, terminology and edge cases the target must encode, cited to source, and produces the hunt list that tells every later stage what to go find. This is the highest-leverage stage in the pipeline; a weak domain brief caps the quality of everything downstream.
---
# bp-domain — master the problem space

## Your job

You are the first stage. **Nobody has looked at the product yet, and that is deliberate.**

If you start from the screens, you will only ever see what the screens show — and the
screens are roughly 15% of the product. The other 85% is the rules the product encodes:
the regulation it must satisfy, the arithmetic that must be exactly right, the edge cases
practitioners hit on day three, the workflow a professional actually runs.

Your output answers: **"What would a system in this space have to get right, whether or
not this particular vendor got it right?"** That becomes the yardstick everything else is
measured against — including the target itself.

You are writing a brief good enough that an engineer who has never heard of this domain
could read it and ask intelligent questions in a room full of practitioners.

## Scope — do only this

- **Deliver:** the cited rules of the problem space, and the hunt list that directs every
  later stage.
- **Do not:** open, crawl, or screenshot the product. That is `recon`'s job, and doing it
  here defeats the reason this stage runs blind. If you catch yourself describing their UI,
  stop — you are out of lane.
- **Emit:** the files under `## Emit`, the `domain` manifest slice, and `DOM-*` ledger lines.
  Nothing else.
- **Stop when:** an engineer new to the domain could ask sharp questions from your brief, and
  every hunt-list item is a concrete thing a later stage can go check. Do not keep researching
  past that.

## Load first

- **`bp-mandate`** — read it first, every time. It tells you the job is authorized and that
  your only real failure mode is not delivering.
- `bp-manifest` (the contract), `bp-evidence` (the proof rules — your prefix is `DOM`)
- From the manifest: `target.url`, and whatever the user said in intake about the product's
  category, geography, and audience.
- You need **web search / fetch**. If you have no web tool, stop and say so — this stage is
  research; without search you would be writing from memory, and memory is not a source.

---

## Method

### 1. Establish what kind of problem this is (30 minutes of reading, no writing)

Identify, from the product's landing page and category:
- **The domain** — capital-gains tax reporting · payroll · lending · logistics · clinical
  scheduling · ad measurement · whatever it is. Be specific: not "fintech", but
  "Indian retail-investor capital-gains computation and ITR filing support".
- **The jurisdiction(s)** — rules are geographic. A payroll product in India and one in
  Germany share almost no logic.
- **The regulated perimeter** — is anyone's money, health, identity, or safety involved?
- **Who is accountable when it is wrong** — the user, their accountant, the vendor, a
  regulator? This tells you which parts must be provably correct rather than merely good.

### 2. Find the governing rules — the actual text, not summaries

This is the part people skip and it is the part that matters.

Search for and read the **primary sources**: the statute, the circular, the standard, the
spec, the scheme document, the regulator's FAQ. Then the practitioner interpretations
(a Big-4 explainer, a professional body's guidance note) for the parts the primary text
leaves ambiguous.

For each rule you find, log a `DOMAIN` claim with the **clause number and a verbatim quote**.
"The law requires FIFO" is not a claim. "s.45(2A) read with Rule 37BA requires FIFO
matching per demat account, quoted: '...' " is a claim.

Go after, at minimum:
- **The computational rules** — every formula, threshold, rate, slab, cut-off date, rounding
  rule, ordering rule. These are where products are actually wrong.
- **The temporal rules** — what changed when, and what grandfathering applies. Almost every
  regulated domain has a "before date X, different rule" seam, and it is a top source of bugs.
- **The identity and eligibility rules** — who qualifies for what treatment. (Resident vs NRI,
  employee vs contractor, insured vs cash-pay.)
- **The reporting obligations** — the exact output artifacts required, and their formats.
  Products live or die on producing the schedule/return/filing correctly.
- **The record-keeping and audit rules** — retention periods, immutability, what must be
  reconstructible years later. These are *architectural* constraints, not features.

### 3. Learn how the work is actually done (the workflow, not the software)

Rules tell you what is correct. Workflows tell you what is usable. Find both:
- **The personas** — not "users", but the actual roles. The individual investor filing once
  a year and the CA filing for 200 clients in eight weeks are different products.
- **The job-to-be-done** — what triggers the work, what "done" looks like, what the
  deadline is, what happens if it slips.
- **Where the data comes from** — practitioners fight upstream data before they compute
  anything. Which formats, which providers, which broken exports, which password-protected
  PDFs. **Import is usually a bigger engineering problem than the domain math.** Enumerate
  every source format you can find evidence of.
- **The reconciliation step** — every serious domain has one: the moment the practitioner
  checks the system against reality. Find out what it is and what it compares.
- Sources: professional forums, subreddits, practitioner blogs, YouTube walkthroughs of the
  *manual* process, industry association material, training courses.

### 4. Name the hard engines (this is the deliverable's spine)

From the rules and the workflow, identify the **3–7 computational cores** that ARE the
product — the parts that take real engineering to get right, where "approximately correct"
means "wrong".

For each, state now (Stage 5 `bp-engines` will go deeper):
- what it computes, in one sentence
- the rules it must implement (by your `DOM` claim ids)
- why it is hard — the specific thing that makes a naive implementation wrong
- your first estimate of difficulty: S / M / L / XL

The test for a hard engine: **if you got it subtly wrong, would the user find out, and would
it matter?** A gains calculator that is off by ₹4,000 fails that test badly. A dashboard chart
that renders 2px off does not. Everything in the second category is not an engine.

### 5. Collect the edge cases practitioners know and users don't

These are the highest-value paragraphs in your brief, because they are the ones a competitor
building from screenshots will miss entirely. Hunt for them specifically: search
`"<domain>" + "edge case" | "gotcha" | "how do I handle" | "doesn't work when"` in forums,
support communities, and professional Q&A.

For each: the situation, why the naive handling is wrong, what correct handling looks like,
and how often it occurs (common / occasional / rare-but-catastrophic).

### 6. Map the compliance perimeter

List every regime a system in this domain triggers, with the trigger condition, the concrete
obligations it imposes, and whether the obligation is **architectural** (must be designed in:
encryption, residency, consent capture, audit logging, retention, deletion) or **procedural**
(can be added later: policies, DPAs, training).

Common triggers — check each: card/payment data → PCI-DSS · EU personal data → GDPR ·
India personal data → DPDP · California → CCPA/CPRA · health data → HIPAA · children →
COPPA · B2B enterprise sales → SOC 2 · investment/securities → the local securities
regulator + KYC/AML · lending → the local banking regulator · tracking/cookies → ePrivacy.

Surface obligations. **Do not give legal advice.** Where you are unsure, write
"needs legal review" and say what specifically needs reviewing.

### 7. Read the landscape

Who else solves this? For each significant competitor: their approach, what they are
known to be good at, what users complain about. This is context for Stage 6 (`bp-gaps`)
and Stage 1 (`bp-intel`) — you are not doing their job, you are giving them a starting map.

### 8. Write the hunt list — the thing that changes the rest of the pipeline

This is why `bp-domain` runs before `bp-recon`. You now know things the crawler could
never infer. Turn them into instructions.

Write `blueprint-out/domain/hunt-list.md` — an explicit checklist for later stages:

```markdown
## For recon (Stage 2)
- [ ] Find the screen where a user resolves a corporate action (bonus/split). Domain says
      this must exist [DOM-034]; if there is no such screen, that is a finding.
- [ ] Capture the import flow for EVERY format listed in domain-brief §3.3. Import is the
      hard part; a demo that only shows one broker is hiding the problem.
- [ ] Look for a "recompute"/"recalculate" action. Its existence tells us whether results
      are stored or derived [feeds DS + ENG].

## For api (Stage 3)
- [ ] Does any endpoint expose the grandfathering FMV [DOM-021]? If the value is computed
      server-side and never returned, the engine is fully backend.

## For datastore (Stage 4)
- [ ] Domain requires 8-year retention with reconstructibility [DOM-052] → look for evidence
      of an append-only ledger / event table, not just mutable rows.

## For engines (Stage 5)
- [ ] Engine "gains-computation" must handle: FIFO per demat account, 112A grandfathering,
      buyback dual-entry, physical→demat with no contract note. Verify each.

## For gaps (Stage 6)
- [ ] Practitioners complain X is manual everywhere in this domain [DOM-061] — check whether
      the target automates it. If not, that is our first add-on.
```

Be concrete and checkable. A hunt-list item that cannot be marked done or not-done is noise.

---

## Proof requirements

- Every rule, rate, threshold, date and obligation is a `DOMAIN` claim with **source URL +
  clause/section + verbatim quote**. No exceptions. A rule without a citation is a rumour,
  and a rumour in a build spec becomes a bug.
- Every workflow/persona/edge-case claim is `EXTERNAL` with source URL + quote (or video URL
  + `mm:ss`).
- Anything you conclude yourself is `INFERRED` with a `basis` list of the claim ids you
  reasoned from.
- **If you cannot find the primary source, say so.** Write the claim at `EXTERNAL` grade
  citing the secondary source, and add it to the brief's "unverified rules" list. A flagged
  gap is useful; a confident paraphrase of a rule you never read is dangerous.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/domain/domain-brief.md` | The main deliverable. Sections: 1 Problem & jurisdiction · 2 Governing rules (cited) · 3 Workflows, personas & data sources · 4 The hard engines · 5 Edge cases & failure modes · 6 Compliance perimeter · 7 Landscape · 8 Glossary · 9 Unverified rules (the honest gaps) |
| `blueprint-out/domain/glossary.md` | Every domain term with its precise meaning. Later stages **must** use this vocabulary — it is also the vocabulary the UI must preserve (see `bp-ux`). |
| `blueprint-out/domain/hunt-list.md` | The per-stage checklist from step 8 |
| `blueprint-out/evidence/ledger.jsonl` | Append your `DOM-*` claims |

Manifest slice `domain`:
```jsonc
"domain": {
  "brief": "blueprint-out/domain/domain-brief.md",
  "glossary": "blueprint-out/domain/glossary.md",
  "hunt_list": "blueprint-out/domain/hunt-list.md",
  "jurisdiction": ["IN"],
  "rules_cited": 47,
  "hard_engines": [
    {"name":"gains-computation","one_liner":"...","difficulty":"XL","rule_claims":["DOM-018","DOM-021"]}
  ],
  "compliance_regimes": [
    {"regime":"DPDP","trigger":"stores Indian investor PII","architectural":true,"claim":"DOM-052"}
  ],
  "unverified_rules": ["..."]
}
```
Then `status.domain = "done"`.

---

## Done when

- [ ] Every hard engine named, with its rules cited by claim id
- [ ] ≥1 primary-source citation for every computational rule the engines depend on
- [ ] Temporal/grandfathering seams identified for each rule that has one
- [ ] All input data sources/formats enumerated
- [ ] ≥10 practitioner edge cases documented (fewer only if the domain is genuinely simple —
      and then say why)
- [ ] Compliance table complete, each obligation marked architectural or procedural
- [ ] Glossary written — later stages have a shared vocabulary
- [ ] `hunt-list.md` has concrete, checkable items for recon, api, datastore, engines, gaps
- [ ] Ledger self-check from `bp-evidence` passes
- [ ] "Unverified rules" section is honest and non-empty unless you truly cited everything

---

## Never

- Never write a rule from memory. Your training data has a cutoff and tax law does not care.
  **Search, read the source, quote it, date it.**
- Never look at the target's screens for your rules. The target may be wrong; you are
  building the yardstick, not copying the answer.
- Never state a rate, threshold, or date without its effective-from date.
- Never give legal advice. Surface obligations, cite the regime, flag for review.
- Never produce a brief that is a summary of the vendor's marketing. If your brief could
  have been written by reading only the product's homepage, you have not done this stage.
