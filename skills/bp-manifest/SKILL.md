---
name: bp-manifest
description: The Blueprint stage contract. How to read/write ./blueprint-out/manifest.json so stages hand off cleanly. Load this in every Blueprint stage.
---
# Blueprint manifest contract

There is ONE shared file: `./blueprint-out/manifest.json`. Every stage:
1. Reads it.
2. Does its work using upstream slices as input.
3. Writes ONLY its own slice + sets `status.<your_stage> = "done"` (or `"failed"`).
4. Never deletes or rewrites another stage's slice.

Full schema: `manifest.schema.json` at the repo root. Slices, in order:
`target` (input) → `recon` → `intel` → `database` → `api` → `dataflow` →
`frontend` → `assembly`.

Rules:
- Paths in the manifest are relative to the run's working directory.
- If your inputs are missing (upstream `status` != "done"), stop and report — do
  not fabricate upstream data.
- Anything not directly observed (from HAR/DOM) is `confidence: "inferred"`.
- Write atomically: read, mutate your slice in memory, write the whole file back.
