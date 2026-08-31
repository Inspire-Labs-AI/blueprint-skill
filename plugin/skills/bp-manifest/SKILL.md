---
name: bp-manifest
description: The Blueprint stage contract. How to read and write ./blueprint-out/manifest.json so twelve stages hand off cleanly without stepping on each other. Load this in EVERY Blueprint stage, alongside bp-evidence.
---
# bp-manifest — the stage contract

## Your job

There is ONE shared state file: `./blueprint-out/manifest.json`. It is how stages talk to
each other. You read the whole thing, you write exactly one slice, you leave everything
else untouched.

Full JSON Schema: `manifest.schema.json` at the repo root. Read it if a field is unclear.

---

## The protocol (do these four things, in this order)

1. **Read** `blueprint-out/manifest.json` in full.
2. **Check your inputs.** Every stage below lists what it requires. If a required
   upstream slice has `status != "done"`, **stop and report** — do not run on missing
   inputs and do not fabricate what upstream should have given you.
3. **Set `status.<your_stage> = "running"`** and write the file back before you start
   real work. This is how a resumed run knows what was interrupted.
4. **Do your work**, then write ONLY your slice + `status.<your_stage> = "done"`
   (or `"failed"` with `errors.<your_stage>` explaining why).

Writing is read-modify-write on the whole file: read it fresh, mutate your slice in
memory, write the whole object back. Never patch blindly — another stage may have
written since you last read.

---

## The stages, in dependency order

| # | Stage key | Skill | Requires | Produces |
|---|---|---|---|---|
| 0 | `domain` | `bp-domain` | — | The rules of the problem space, cited |
| 1 | `intel` | `bp-intel` | `domain` | Positioning + behavioural feature inventory |
| 2 | `recon` | `bp-recon` | `domain`, `intel` | Screens, network capture, DOM, bundles |
| 3 | `api` | `bp-reverse-api` | `recon` | Proven endpoint contracts + typed client |
| 4 | `datastore` | `bp-datastore` | `api`, `domain`, `intel` | DB technology + schema, from evidence |
| 5 | `engines` | `bp-engines` | `domain`, `api`, `datastore` | The computational cores + worked examples |
| 6 | `gaps` | `bp-gaps` | `intel`, `recon`, `engines` | What they get wrong → our add-ons |
| 7 | `dataflow` | `bp-dataflow` | `recon`, `api`, `datastore` | Supporting UI↔API↔store map |
| 8 | `ux` | `bp-ux` | `intel`, `recon`, `gaps` | Familiar-but-better design spec |
| 9 | `spec` | `bp-blueprint` | all of the above | `PLAN.md` + `PRD.html` — the deliverable |
| — | **GATE** | — | `spec` | Human approval. Nothing below runs without it. |
| 10 | `frontend` | `bp-frontend-build` | `ux`, `dataflow`, `api` | The app UI |
| 11 | `assembly` | `bp-assemble` | `frontend`, `api`, `datastore`, `engines` | Runnable repo + conformance results |

Stages 3 and 4 both depend on `recon` but `datastore` also wants `api`, so run
`api` first. Stages 5 (`engines`) and 7 (`dataflow`) are independent and may run
concurrently; stage 6 (`gaps`) requires `engines`, so it starts once `engines` is `done` —
it is not a peer of the other two.
Stage 8 needs `gaps`.

---

## Partial runs — the table above is a dependency graph, not a schedule

**Most runs are not the full twelve stages.** The user asks for a PRD, or a quick look, or
just "what database are they using". Treat the table as a graph and resolve it:

1. **Identify the target stage** — the one whose output answers the request.
2. **Walk its `Requires` column transitively** to get the full prerequisite set.
3. **Drop anything already `done`** in the manifest. This is what makes runs resumable and
   composable — an `explore` yesterday means today's `prd` only runs what is missing.
4. **Run the remainder in dependency order**, concurrently where the graph allows.

So "what DB do they use?" resolves to `datastore` → needs `api`, `domain`, `intel` → `api`
needs `recon` → `recon` needs `domain`, `intel`. Five stages, not twelve, and if `domain`
and `intel` are already `done`, three.

**Depth scales with the ask.** The same stage runs differently in a 15-minute `explore`
than in a `build`. Each skill's Method is written for full depth; when running shallow,
do the numbered steps in order and stop early rather than doing all of them badly. Then
record honestly in the manifest what depth you ran:

```jsonc
"status": { "recon": "done" },
"depth":  { "recon": "shallow" }   // shallow | standard | deep
```

A later stage that needs more than `shallow` gives you may re-run the upstream stage at
greater depth. That is normal and expected — say so rather than working around thin inputs.

**Never fabricate a skipped stage.** If a stage is `pending` and you need its output,
either run it or declare the gap. Writing plausible content into another stage's slice is
the one unrecoverable failure in this pipeline.

---

## Slice-writing rules

- **Paths** in the manifest are relative to the run's working directory, always starting
  `blueprint-out/`. Never absolute.
- **Every substantive value carries its evidence.** Where the schema offers an
  `evidence` field, fill it with the claim ids you logged in
  `blueprint-out/evidence/ledger.jsonl` (see `bp-evidence`). A manifest value with no
  claim id behind it is unverifiable and will be rejected by the supervisor.
- **Confidence is explicit.** Anything not directly observed is marked
  `confidence: "inferred"` (or `"low"`/`"medium"`/`"high"` where the schema asks for a
  level). Silence is not confidence.
- **Never delete or rewrite another stage's slice.** If you believe an upstream slice is
  wrong, write your correction into `disputes` (array of
  `{stage, path, upstream_value, your_value, reasoning, claim_ids}`) and tell the
  supervisor. Do not silently overwrite.
- **Failures are informative.** `status.<stage> = "failed"` must come with
  `errors.<stage>` = what you tried, what happened, what would unblock it. "Failed" with
  no explanation is the same as lying.

---

## Initialising (supervisor / workflow only)

```jsonc
{
  "target": { "url": "<url>", "extra_urls": [], "auth": null },
  "goal": "functional parity + add-ons",
  "status": { "domain":"pending","intel":"pending","recon":"pending","api":"pending",
              "datastore":"pending","engines":"pending","gaps":"pending",
              "dataflow":"pending","ux":"pending","spec":"pending",
              "frontend":"pending","assembly":"pending" },
  "gate": { "approved": false, "scope": null }
}
```

`target.auth` is non-null **only** when the user has confirmed authorization, and then
carries `{authorized: true, login_url, notes}`. Its presence is what unlocks authenticated
capture. Never set it yourself.

`gate.approved` flips to `true` only by explicit human answer. Stages 10–11 must refuse to
run while it is `false`.

---

## Never

- Never run a stage whose required upstream slices are not `done`.
- Never write a value you cannot trace to a ledger claim id.
- Never touch `target`, `gate`, or another stage's slice.
- Never report `done` when you produced partial output — report `done` with an explicit
  `coverage` note, or `failed`. A silent partial is the worst outcome in this pipeline.
