---
name: bp-engines
description: Stage 5 — specify the computational cores that ARE the product. For each of the 3-7 hard engines, states what it computes, the exact algorithm, the rules it implements with citations, the edge cases, a fully worked numeric example, and golden test cases that become the build's conformance suite. This is the stage that separates a spec you can build from a description of some screens.
---
# bp-engines — specify what the product actually computes

## Your job

Every serious product has a small number of computational cores that ARE the product.
The tax engine. The matching algorithm. The pricing rules. The import parser. The
settlement logic. Everything else — auth, CRUD, lists, settings — is scaffolding that any
competent team builds in a week.

**Your job is to specify those cores precisely enough that an engineer can implement them
correctly without ever seeing the original product.**

The test for whether you have done this: *could someone build this engine from your
document, run your worked example, and get the same number?* If not, you have written a
description, not a specification.

## Load first

- **`bp-mandate`** — read it first. Where an engine runs server-side and you cannot see it,
  you specify what it *must* do from the domain research and mark it `INFERRED`. You do not
  stop, and you do not guess and present the guess as observation.
- `bp-manifest`, `bp-evidence` (your prefix is `ENG`)
- `blueprint-out/domain/domain-brief.md` — **the rules live here, cited.** This is your
  primary source. The product is one implementation of these rules; the rules are the truth.
- `blueprint-out/domain/hunt-list.md` — the engine-specific items
- `blueprint-out/api/endpoints.md` + `flows.md` — the inputs and outputs of each engine, and
  which ones run server-side
- `blueprint-out/datastore/` — whether results are computed or stored, and what is persisted
- `blueprint-out/recon/samples/responses/` — **real numbers in and out. These are your test
  vectors.** Nothing else in the run is as valuable for this stage.

---

## Method

### 1. Identify the engines

Start from the candidates `bp-domain` named, then check the evidence:

An engine qualifies if **all three** are true:
1. It transforms inputs into outputs by non-trivial rules (not a lookup, not a format change).
2. Getting it subtly wrong produces a **plausible but incorrect** result — one a user would
   act on and might not catch.
3. It matters. Someone is worse off if it is wrong: financially, legally, medically,
   operationally.

Test it: *if this were off by 3%, would anyone be harmed, and would they notice?* A gains
calculation off by 3% fails badly. A chart 3px off does not. Only the first is an engine.

Expect 3–7. If you have found fifteen, you are counting features. If you have found one, look
harder — the import/ingest path is an engine in almost every product and is routinely missed
because it looks like plumbing. **It is usually the hardest part of the build.**

Common engine shapes, to prompt your search: computation/tax/pricing · matching/allocation ·
parsing/ingest of messy third-party formats · scheduling/optimisation · reconciliation ·
risk/eligibility scoring · settlement/ledger · search relevance · forecasting.

### 2. Specify each engine

Fill this completely. A missing row is a hole an engineer will fill by guessing.

```markdown
## ENG-01 · Capital-gains computation

**What it computes** — one sentence.

**Why it is hard** — the specific thing that makes a naive implementation wrong. Be concrete.
"You cannot just subtract cost from proceeds, because lots must be matched FIFO per demat
account, and pre-2018 holdings are grandfathered against a fixed FMV [DOM-021]."

**Inputs** — every input: source, type, units, precision, and what happens when it is
missing or malformed. Where does each come from — user, import, another engine, a table?

**Outputs** — every output: type, units, precision, rounding rule, and where it goes
(displayed, stored, fed to another engine, exported to a filing).

**Rules implemented** — a numbered list. Each rule cites its `DOM-*` claim. Each is stated
as a condition and a consequence, not as prose. This is the load-bearing section.

  R1. Lots are matched first-in-first-out **within a demat account**, never across [DOM-018]
  R2. For equity acquired on or before 31-Jan-2018, cost = max(actual cost, FMV on
      31-Jan-2018), capped at sale proceeds [DOM-021]
  R3. Holding period > 12 months → long-term; else short-term [DOM-019]
  ...

**Algorithm** — numbered steps or pseudocode. Explicit ordering. Explicit tie-breaks.
Explicit rounding, and **at which step** rounding happens (this changes the answer).
Explicit units. An engineer must be able to type this in.

**Edge cases** — a table: situation · why naive handling is wrong · correct handling ·
frequency · claim id. Aim for ten or more on a real engine.

**Failure modes** — what happens with bad input, missing data, or a rule with no applicable
branch. Does it fail loudly, skip the row, or flag for user review? For anything financial
or regulated, **silent wrong answers are the worst outcome** — specify loud failure.

**Worked example** — see step 3. Mandatory.

**Golden tests** — see step 4. Mandatory.

**Reproduction difficulty** — S / M / L / XL, with the reason. What specifically takes the
time: the rule count, the edge cases, the reference data needed, or the test surface?

**Observability** — did we see this run? `OBSERVED` (we have real inputs and outputs from
the API), `INFERRED` (server-side, we specify from the domain), or partial. Say which.
```

### 3. The worked example — mandatory, with real numbers

Take a realistic case and run the algorithm by hand, showing **every intermediate value**.

```markdown
### Worked example — ENG-01

Input: 3 buys and 1 sell of RELIANCE in demat account A.
  2017-06-12  BUY   100 @ ₹780.00   (pre-2018 → grandfathering applies, R2)
  2019-03-04  BUY   50  @ ₹1,240.00
  2021-08-20  BUY   80  @ ₹2,010.00
  2024-11-15  SELL  120 @ ₹2,850.00
Reference: FMV on 31-Jan-2018 = ₹962.40 [source: BSE bhavcopy 31-Jan-2018]

Step 1 — FIFO match 120 units within account A (R1):
   100 from the 2017-06-12 lot, 20 from the 2019-03-04 lot.

Step 2 — lot 1 (100 units, pre-2018 → R2):
   actual cost      = 100 × 780.00   = ₹78,000.00
   FMV 31-Jan-2018  = 100 × 962.40   = ₹96,240.00
   proceeds         = 100 × 2,850.00 = ₹2,85,000.00
   grandfathered cost = min(max(78,000, 96,240), 2,85,000) = ₹96,240.00
   holding period 2017-06-12 → 2024-11-15 = 7.4 yr > 12 mo → LONG TERM (R3)
   gain = 2,85,000 − 96,240 = ₹1,88,760.00

Step 3 — lot 2 (20 units, post-2018 → actual cost):
   cost     = 20 × 1,240.00 = ₹24,800.00
   proceeds = 20 × 2,850.00 = ₹57,000.00
   holding period 2019-03-04 → 2024-11-15 = 5.7 yr → LONG TERM
   gain = 57,000 − 24,800 = ₹32,200.00

Step 4 — aggregate, round half-up to 2dp at the final step only (R7):
   total long-term gain = ₹2,20,960.00
   total short-term gain = ₹0.00

Expected output: { ltcg: 220960.00, stcg: 0.00, lots_matched: 2, remaining_units: 110 }

Naive implementation using average cost instead of FIFO: ₹2,04,880.00 — **₹16,080 wrong**,
and plausible enough that nobody catches it.
```

That last line is the point of the whole exercise. **Show what a wrong implementation
produces, so the reader understands why the detail matters.**

If you captured real inputs and outputs from the API, use those and state that the expected
output is `OBSERVED`. That is the strongest possible form of this section — you are proving
your specification reproduces their actual behaviour.

### 4. Golden tests

Turn the worked example and every edge case into concrete test vectors:

```yaml
- id: ENG-01-T003
  name: pre-2018 lot where FMV exceeds sale proceeds (R2 cap applies)
  input:  { buys: [...], sell: {...}, fmv_2018: 3100.00 }
  expect: { ltcg: 0.00, note: "cost capped at proceeds, gain floored at zero" }
  rule:   R2
  source: DOM-021
  observed: false
```

Write these to `blueprint-out/engines/golden/<engine>.yaml`. **`bp-assemble` runs them
against the build.** This is what makes "it compiles" stop being the definition of success.

Minimum: the worked example, every edge case, both boundaries of every threshold, and one
malformed-input case per engine.

### 5. Verify against observed behaviour

Where you have real input/output pairs from `recon/samples/responses/`, **run your specified
algorithm against them by hand and check it produces their number.**

- **It matches** → your specification is validated. Say so; this is the strongest claim in
  the whole run.
- **It does not match** → one of three things, and you must determine which:
  1. Your understanding of the rule is wrong → fix the spec.
  2. Their implementation is wrong → **this is a major finding.** Log it, hand it to
     `bp-gaps`. Correctness is the most defensible add-on there is.
  3. There is a rule you have not found → go back to the domain brief and search again.

Never leave a mismatch unexplained. An unexplained mismatch means the engine is not specified.

### 6. Size the build

Per engine: effort (Cx + days, optimistic → realistic), what reference data must be
sourced (price histories, rate tables, holiday calendars, format specs), the test surface,
and the ongoing maintenance burden (do the rules change annually?).

**The engines are where build estimates go wrong.** A team that budgets two weeks for "the
calculations" and finds forty edge cases and a required reference-data pipeline is the normal
outcome. Say so plainly.

---

## Proof requirements

- Every rule cites a `DOM-*` claim with clause and quote, or an `OBSERVED` behaviour with an
  anchor. **A rule with neither does not go in the spec.**
- Every worked example is arithmetically correct. **Check the arithmetic.** A worked example
  with a wrong number is worse than none — it will be copied into tests and become the bug.
- Every engine states its observability honestly: did you see it run, or are you specifying
  from the rules?
- Where your spec disagrees with observed behaviour, both are recorded plus your adjudication.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/engines/engines.md` | All engine specifications |
| `blueprint-out/engines/golden/<engine>.yaml` | Test vectors, one file per engine |
| `blueprint-out/engines/verification.md` | Spec-vs-observed comparisons and adjudications |
| `blueprint-out/evidence/ledger.jsonl` | Append `ENG-*` |

Manifest slice `engines`:
```jsonc
"engines": {
  "doc":"blueprint-out/engines/engines.md", "golden_dir":"blueprint-out/engines/golden",
  "engines":[{
    "id":"ENG-01","name":"capital-gains-computation","difficulty":"XL",
    "rules":12,"edge_cases":14,"golden_tests":23,
    "observability":"partial","server_side":true,
    "rule_claims":["DOM-018","DOM-019","DOM-021"],
    "verified_against_observed":true,
    "reference_data_needed":["BSE/NSE FMV 31-Jan-2018","ISIN master"],
    "estimate_days":{"optimistic":18,"realistic":34}
  }],
  "total_golden_tests":68,
  "mismatches_found":[{"engine":"ENG-01","note":"their output ignores the proceeds cap in R2","claim":"ENG-044","to_gaps":true}]
}
```
Then `status.engines = "done"`.

---

## Done when

- [ ] 3–7 engines identified, each passing the three-part test
- [ ] The import/ingest path considered as an engine (it usually is one)
- [ ] Every engine has inputs, outputs, numbered cited rules, and a step-by-step algorithm
- [ ] Every engine has a worked example with real numbers and **verified arithmetic**
- [ ] Every engine shows what a naive implementation gets wrong
- [ ] ≥10 edge cases per substantial engine
- [ ] Rounding rules and the step at which rounding occurs are explicit
- [ ] Golden test vectors written for every engine
- [ ] Spec checked against observed outputs wherever pairs exist; every mismatch adjudicated
- [ ] Mismatches attributable to *their* error handed to `bp-gaps`
- [ ] Reference data requirements listed
- [ ] Per-engine estimates with reasoning
- [ ] Ledger self-check passes

---

## Never

- Never write "implements standard FIFO accounting" and move on. **Write the algorithm.**
  If the reader has to look up how it works, you have not specified it.
- Never skip the worked example because the algorithm "seems clear". It never is, and the
  example is what catches your own misunderstanding.
- Never present an unverified arithmetic result. Check it.
- Never let a spec-vs-observed mismatch go unexplained.
- Never treat the import parser as plumbing. It is usually the largest single risk in the
  build and the reason products in messy-data domains take a year instead of a quarter.
- Never round intermediate values unless the rule says to. Say explicitly where rounding
  happens — it changes the answer and it is a classic source of silent divergence.
