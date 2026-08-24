---
name: bp-dataflow
description: Stage 4 fusion. Correlates every UI element to its data fields, serving API endpoint, and backing DB tables into one end-to-end map + Mermaid diagram.
---
# bp-dataflow — the fusion step (the whole point)

No external tool — this is pure correlation reasoning over the manifest. Read
`recon` (screenshots + DOM), `intel` (features), `database` (tables/columns), `api`
(endpoints). For each visible UI surface, answer: what data does it show → which
endpoint serves that data → which table(s) store it.

## Method
1. Enumerate UI elements per screenshot (cards, tables, forms, lists, detail views).
2. For each, list the `data_fields` it renders (read labels/values from DOM).
3. Match fields to an `api_endpoint` — `observed` if that endpoint appears in the
   HAR/DOM fetches, else `inferred` from naming + REST conventions.
4. Match fields to `db_tables` from the Stage-2 schema (column-name overlap).
5. Tag each entry `observed` or `inferred`.

## Emit
- `blueprint-out/dataflow/diagram.mmd` — Mermaid `flowchart LR` of UI -> API -> DB.
- Manifest `dataflow.map` (array) + `dataflow.diagram` (path); `status.dataflow="done"`.

This map is the build spec for Stage 5/6 — every frontend section reads it to know
what data to fetch and from where.
