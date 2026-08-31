---
name: bp-dataflow
description: Stage 7 — the wiring map. Correlates each screen and component to the endpoints it calls and the stores those read, so the build knows what to fetch where. A supporting artifact for implementation, not a source of product understanding - the mechanism lives in bp-engines, the contracts in bp-reverse-api, the storage in bp-datastore.
---
# bp-dataflow — the wiring map

## Your job

Produce the map an implementer needs: **for each screen, what does it load, from which
endpoint, backed by which table or collection, and in what order.**

Know what this is and is not. This is **plumbing documentation**. It says a card renders
`total_gain` from `GET /portfolio` backed by `holdings`. It does not say how `total_gain` is
computed — that is `bp-engines`, and that is where the product actually lives.

Do not mistake this map for the product. Treating the wiring as the meaning is how a rebuild
ends up with a perfect-looking dashboard full of wrong numbers — the numbers come from the
engines, not the wiring. This stage is useful, and it is not the value.

## Scope — do only this

- **Deliver:** the wiring map — per screen, what it loads, from which endpoint, backed by
  which store, in what order.
- **Do not:** explain how any value is computed (that is `engines`), or redesign the screens
  (that is `ux`). This is plumbing documentation. When you find a computed field, flag it and
  point at the engine — do not derive it.
- **Emit:** the files under `## Emit`, the `dataflow` slice, and `FLW-*` ledger lines.
- **Stop when:** every captured screen is mapped and marked observed/inferred, with waterfalls
  noted. This stage is useful and it is not the product's meaning — do not inflate it into one.

## Load first

- **`bp-mandate`**, `bp-manifest`, `bp-evidence` (your prefix is `FLW`)
- `blueprint-out/recon/` — screenshots, DOM, HAR (**the HAR tells you what each screen
  actually loaded — use it, do not guess from labels**)
- `blueprint-out/api/endpoints.md`
- `blueprint-out/datastore/schema.prisma` + `field-provenance.md`
- `blueprint-out/ux/screens.md` — if `ux` has run, map to **our** screens; otherwise theirs

---

## Method

1. **Per screen, read the HAR.** Filter the capture by the page's navigation and list every
   request it fired, in order, with its timing. That is the ground truth of what the screen
   loads — far better than inspecting labels.
2. **Per component**, list the fields it renders (from the DOM) and match them to fields in
   the response bodies. Match by name first, then by value — **if a rendered value appears
   verbatim in a response body, that is a proven match**; anchor it.
3. **Map fields to storage** using `field-provenance.md`. Mark fields that are computed and
   not stored — those point at an engine.
4. **Record the load sequence**: what is fetched on mount, what is deferred, what is
   parallel, what waterfalls (a request that cannot start until a previous one returns).
   **Waterfalls are the main cause of slow screens** — note each one; it is a `bp-gaps` input
   and a design constraint for our build.
5. **Note over- and under-fetching**: a list endpoint returning 60 fields to render 4, or a
   screen making 30 calls that one endpoint could serve. Both are build decisions for us.
6. **Flag every unmatched field**, both directions:
   - Rendered but not found in any response → computed client-side, or from an endpoint you
     did not capture. Say which.
   - Returned but never rendered → an unused field, a hidden feature, or over-fetching.
     Sometimes a returned-but-unrendered field reveals a capability the UI does not expose.
7. **Draw the diagram** — Mermaid `flowchart LR`, screen → endpoint → store. Group by area.
   If the product is large, one diagram per area beats one unreadable diagram.

---

## Proof requirements

- A mapping is `observed` when the endpoint appears in the HAR for that screen **and** the
  rendered value appears in its response. Anchor both.
- A mapping guessed from field names and REST conventions is `inferred`. Say so per row.
- Table mappings come from `field-provenance.md`, not from name similarity.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/dataflow/map.md` | The screen → component → fields → endpoint → store table |
| `blueprint-out/dataflow/diagram.mmd` | Mermaid flowchart(s) |
| `blueprint-out/dataflow/load-sequences.md` | Per screen: order, parallelism, waterfalls, timings |
| `blueprint-out/evidence/ledger.jsonl` | Append `FLW-*` |

Manifest slice `dataflow`:
```jsonc
"dataflow": {
  "map":"blueprint-out/dataflow/map.md","diagram":"blueprint-out/dataflow/diagram.mmd",
  "entries":[{"screen":"/holdings","component":"holdings table","fields":["isin","qty","avg_cost"],
              "endpoint":"GET /v2/holdings","stores":["holdings"],
              "confidence":"observed","anchors":["har:recon/traffic.har#288"]}],
  "counts":{"observed":142,"inferred":31},
  "waterfalls":[{"screen":"/reports/capital-gains","depth":3,"total_ms":4200,"claim":"FLW-061"}],
  "client_computed_fields":["portfolio.day_change_pct"],
  "unrendered_fields":[{"endpoint":"GET /v2/holdings","field":"internal_risk_band","note":"never displayed"}]
}
```
Then `status.dataflow = "done"`.

---

## Done when

- [ ] Every captured screen mapped
- [ ] Every mapping marked `observed` or `inferred`, with anchors on the observed ones
- [ ] Load sequences recorded; waterfalls identified with timings
- [ ] Client-computed fields flagged (they point at engines)
- [ ] Unrendered returned fields flagged (they point at hidden capability)
- [ ] Diagram renders
- [ ] Ledger self-check passes

---

## Never

- Never claim this map explains the product. It explains the wiring.
- Never guess a table from a field name when `field-provenance.md` has the answer.
- Never mark a mapping `observed` without the HAR entry to back it.
- Never quietly skip screens that were behind auth — list them as unmapped.
