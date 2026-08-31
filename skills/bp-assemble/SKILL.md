---
name: bp-assemble
description: Stage 11 — wire the frontend, typed client, schema and backend into one runnable repo, then prove it behaves correctly by running the golden test vectors from bp-engines. Success is conformance, not compilation - a build that passes typecheck with every business rule stubbed is a failure, and this stage is what says so.
---
# bp-assemble — wire it up, then prove it works

## Your job

Two parts, and the second is the one that matters.

1. **Wire** — frontend + typed client + schema + backend into one repo that runs.
2. **Prove** — run every golden test vector from `bp-engines` against the implementation and
   report pass/fail per engine.

**"It compiles" is not success.** A repo that typechecks cleanly with every engine stubbed
is a demo, and reporting it as done is the failure this pipeline was rebuilt to prevent.
Your headline number is **conformance**, not build status.

## Gate check — do this first

```
Read manifest → if gate.approved !== true → STOP.
```

## Scope — do only this

- **Deliver:** one runnable repo, and a conformance report from running every golden vector.
- **Do not:** run before `gate.approved === true`. Do not report success on a passing build,
  fake an engine to make the demo look complete, or edit a golden vector's expected value to
  turn a failure green. Your headline number is conformance, not build status.
- **Emit:** `blueprint-out/app/`, `CONFORMANCE.md`, and the `assembly` slice.
- **Stop when:** every engine is either implemented from spec or stubbed with a throwing
  `NotImplementedError`, the vectors have been run, and `honest_summary` reflects reality
  including what is stubbed. No engine returns a plausible wrong value.

## Load first

- **`bp-mandate`**, `bp-manifest`, `bp-evidence`
- `blueprint-out/frontend/` · `blueprint-out/api/client.ts` ·
  `blueprint-out/datastore/schema.prisma` · `blueprint-out/dataflow/map.md`
- `blueprint-out/engines/engines.md` + **`blueprint-out/engines/golden/`** — the algorithms
  to implement and the vectors that judge them

---

## Method

### 1. Assemble

1. `frontend/` → `blueprint-out/app/`
2. `api/client.ts` → `app/lib/api/`
3. `schema.prisma` → `app/prisma/schema.prisma`; generate the client; write migrations
4. Using `dataflow/map.md`, replace placeholder data calls with real client methods
5. `app/.env.example` — API base URL, DB URL. **Never real secrets.**
6. `README.md` — what this is, what is real, what is stubbed, how to run it

### 2. Backend

Implement route handlers for the contracts in `api/endpoints.md`:
- `OBSERVED` + `verified` endpoints → implement against the real contract
- everything else → typed fixture responses, each route marked `mock` in code **and** in a
  response header (`X-Blueprint-Mock: true`) so nothing is mistaken for real at runtime
- error responses follow the taxonomy from `api/conventions.md` — the frontend's error
  states depend on them

### 3. Implement the engines — or stub them loudly

For each engine in `engines.md`, in priority order:

- **Implement it from the specification**: the numbered rules, the algorithm, the rounding
  and the ordering. The spec was written to be typed in; type it in.
- **If you cannot** — out of scope, missing reference data, too large — write a stub that
  **throws** `NotImplementedError("ENG-01: capital-gains computation — see engines.md")`.

**Never return a plausible wrong number.** A stub that throws is honest and safe. A tax
figure that is confidently wrong is the worst artifact this pipeline can produce — someone
will act on it. If a value cannot be computed correctly, it does not get returned.

Reference data the engines need (rate tables, FMV histories, format specs, calendars) goes
in `app/data/` with its provenance, or is listed as required-and-missing.

### 4. Run conformance — the actual deliverable

Turn `engines/golden/*.yaml` into a runnable test suite (`app/tests/conformance/`), run it,
and record the results:

```markdown
| Engine | Tests | Pass | Fail | Not implemented | Verdict |
|---|---|---|---|---|---|
| ENG-01 capital-gains | 23 | 21 | 2 | 0 | ⚠️ two edge cases fail — see below |
| ENG-02 import-parser | 18 | 18 | 0 | 0 | ✅ conformant |
| ENG-03 reconciliation | 12 | 0 | 0 | 12 | ⛔ not implemented (stub throws) |
```

For every failure: the vector, expected vs actual, and the diagnosis — is the implementation
wrong, or is the spec wrong? **Do not fix a failure by editing the expected value.** If the
spec is genuinely wrong, that is a finding: fix `engines.md`, note the correction in the
ledger, and re-run.

### 4b. Parity gates and the parity number — the loop's oracle

Per-engine conformance is necessary and not sufficient. Ship a single **parity number** and a
set of **gates** so "how close are we?" has a computed answer, not an opinion.

**The parity number** — count, do not estimate. Each term is `passing / specified`, from a
test result, never a self-report:

```
parity = features_passing/features_specified · endpoints_conformant/endpoints_contracted ·
         states_reachable/states_specified · engines_conformant/engines_identified
```

Report every denominator. A 95% against a spec that is 60% inferred is 95% confidence in a
partly-guessed target — say so; the parity number rides on the coverage register, not above it.

**Parity gates** — order the build by dependency, not by visibility, and end each phase in a
**testable condition** that must pass before the next phase starts. In a system where a wrong
number is worse than a missing feature, correctness debt compounds faster than feature debt,
so a gate is executable, not a checkbox. Gates come from `bp-engines`' invariants and worked
examples; write them as real tests. Shapes that work:

- **Invariant gate** — the domain invariants as executable assertions: a randomised sequence
  of N create/edit/delete operations leaves every invariant true.
- **Golden-fixture gate** — a realistic seeded fixture (built from the real input samples
  `recon` captured) reproduces a hand-computed result **to the last unit** — to the paisa, to
  the cent, to the row.
- **Negation gate** — a thing that must *not* change stays fixed (the price feed being down
  changes no realised total; a back-dated insert changes every subsequent day and nothing
  before it).

**The loop.** A gate that fails is work, not a verdict: diagnose, fix, re-run — the same
`validator → fix → re-run` loop, now against the gate — until it passes or you can prove it
cannot (missing reference data, an unobservable engine). Then stop and say which, with the
parity number as it stands. Never edit a gate's expected value or lower its bar to pass it;
never mark a phase gated-green while its gate is red. Termination is honest — a plateaued
parity number with the reason named beats a forced 100%.

### 5. Verify it runs

`npm install && npm run build && npm run typecheck`, migrations apply, dev server starts,
and every route in `ia-map.md` loads without a console error. Then walk the primary flows by
hand and confirm they work end to end.

---

## Emit

```
blueprint-out/app/          # the runnable repo
blueprint-out/app/tests/conformance/
blueprint-out/CONFORMANCE.md
```

Manifest slice `assembly`:
```jsonc
"assembly": {
  "repo_path":"blueprint-out/app","run_cmd":"cd blueprint-out/app && npm run dev",
  "wired":true,"build_passes":true,"typecheck_passes":true,
  "conformance":{"total":68,"passed":51,"failed":5,"not_implemented":12,
                 "by_engine":[{"id":"ENG-01","passed":21,"failed":2,"verdict":"partial"}]},
  "engines_implemented":["ENG-01","ENG-02"],
  "engines_stubbed":["ENG-03"],
  "mock_routes":26,"real_routes":41,
  "reference_data_missing":["BSE FMV 31-Jan-2018 series"],
  "honest_summary":"UI complete. 2 of 3 engines implemented; gains engine fails 2 grandfathering edge cases. Reconciliation engine stubbed — needs the FMV dataset."
}
```
Then `status.assembly = "done"`.

`honest_summary` is what the user reads first. Write it accordingly.

---

## Done when

- [ ] Gate verified before any work
- [ ] Repo assembled, migrations apply, dev server runs
- [ ] Every route loads without console errors
- [ ] Mock routes marked in code and by response header
- [ ] Every engine either implemented from spec or stubbed with a throwing `NotImplementedError`
- [ ] **No engine returns a plausible wrong value**
- [ ] Conformance suite generated from the golden vectors and executed
- [ ] `CONFORMANCE.md` written, every failure diagnosed
- [ ] No expected value was edited to make a test pass
- [ ] `honest_summary` reflects reality, including what is stubbed

---

## Never

- Never report success on the basis of a passing build.
- Never fake an engine to make the demo look complete.
- Never edit a golden vector's expected value to turn a failure green.
- Never leave a mock route indistinguishable from a real one at runtime.
- Never write real secrets into the repo.
- Never round or soften the conformance numbers. The failures are the most useful output of
  this entire stage.
