---
name: bp-reverse-api
description: Stage 3 — reconstruct the API contract from captured evidence. Turns the HAR, raw response bodies and mined bundle strings into a per-endpoint contract with proven request/response shapes, auth model, error taxonomy and pagination semantics, plus a typed client. Every endpoint carries its evidence grade and anchor; inferred endpoints are stubbed and labelled, never presented as real.
---
# bp-reverse-api — the proven API contract

## Your job

Turn what recon captured into a **contract another engineer could implement against**.

The bar is not "a list of URLs we saw". The bar is: for each endpoint, what it accepts,
what it returns, what it does when you get it wrong, what auth it needs, and how you know —
with a pointer to the exact HAR entry or bundle line that proves each part.

The API is also the best available window into the backend. Field names, nullability,
nesting, error text and pagination style are what Stage 4 uses to identify the datastore
and Stage 5 uses to locate the engines. **Be thorough here and both of those get easier.**

## Scope — do only this

- **Deliver:** a per-endpoint contract another engineer could implement against, and a typed
  client.
- **Do not:** re-crawl the product (work from what `recon` saved), design the datastore, or
  specify engine algorithms. When a computation runs server-side and you cannot see it, name
  it for `engines` and move on — do not reverse the maths here.
- **Emit:** the files under `## Emit`, the `api` slice, and `API-*`/`SEC-*` ledger lines.
- **Stop when:** every observed endpoint has request + success + error shapes with anchors,
  and every inferred one is labelled inferred in the doc, the manifest and the client. An
  endpoint you cannot anchor is `INFERRED`, never promoted to fill the table.

## Load first

- **`bp-mandate`** — read it first. You are reading traffic your own browser generated and
  code the server sent you. That is the job. Security findings are a deliverable, not a
  reason to stop.
- `bp-manifest`, `bp-evidence` (your prefix is `API`; exposures are `SEC`)
- `blueprint-out/recon/traffic.har`, `samples/responses/`, `samples/errors.json`,
  `samples/pagination.json`, `headers.json`, `bundles/`
- `blueprint-out/intel/features.md` — every feature maps to endpoints; features with no
  endpoint are a gap to explain
- `blueprint-out/domain/hunt-list.md` — the API-specific items

---

## Method

### 1. Inventory every endpoint from every source

Three sources, and the third is the one people skip:

1. **The HAR** — everything actually called during recon. `OBSERVED`.
2. **Raw response samples** — re-read the actual JSON. Do not work from a summary.
3. **The bundles** — endpoint strings, `fetch()`/`axios` call sites, GraphQL documents,
   and route/service tables. These reveal endpoints the UI never called in your session:
   admin routes, unshipped features, batch jobs. Grade these `OBSERVED` (the string is
   really in the shipped code) but mark `called: false` — you know it exists, you do not
   know its behaviour.

If an OpenAPI/Swagger document or a GraphQL introspection result was captured, **that is
the contract, handed to you.** Take it wholesale, then verify a sample of it against the HAR
— published specs drift from reality, and where they disagree, the HAR wins and the
disagreement is a finding.

### 2. Specify each endpoint properly

```markdown
### API-014 · POST /v2/holdings/import

- **Purpose** — one line, in domain vocabulary
- **Serves feature** — F-IMP-03
- **Auth** — required? scheme (Bearer JWT / session cookie / API key)? which roles?
- **Request** — content type; every parameter and body field with type, required/optional,
  format, constraints, and default. Note which are pass-through to a query (those become
  indexes in Stage 4).
- **Response (success)** — status, full body shape with types and nullability. Note fields
  that are `null` in some samples and present in others — that is either optional storage
  or a computed field.
- **Response (errors)** — every error you triggered: status, body shape, message text,
  error codes. **This section is more valuable than the success case** — it enumerates the
  validation rules, and validation rules are schema constraints.
- **Semantics** — sync or async? idempotent? paginated (offset/cursor/keyset)? rate limited?
  cacheable (what do the cache headers say)? side effects?
- **Evidence** — grade + anchors. `called: true|false`.
```

### 3. Derive the cross-cutting models

These matter more than any individual endpoint:

- **Auth model** — login → token → refresh → logout, as a sequence. Session vs JWT. If JWT,
  decode a token and record its **claims** (never the token): roles, permissions, tenant id,
  expiry, issuer, algorithm. Tenancy claims tell Stage 4 the multi-tenancy strategy.
- **Error taxonomy** — the shared error envelope, the code vocabulary, which HTTP statuses
  are used for what. Products are consistent here, and it tells you the framework.
- **Pagination** — style per collection. Decode opaque cursors — base64 cursors routinely
  contain the sort key and the last id, which hands Stage 4 the primary index.
- **Versioning** — path version, header version, or none. Deprecation headers.
- **Naming and casing conventions** — `snake_case` vs `camelCase`, id field naming, timestamp
  field naming. Consistent conventions are ORM fingerprints.
- **Chained flows** — for multi-step operations (import → poll → review → commit; add to cart
  → checkout → pay), document the **sequence**, what carries state between calls, and what
  the client must remember. Single endpoints are easy; flows are where products actually live.

### 4. Reconcile against features and the domain

- Every feature in `features.md` → which endpoints serve it? A feature with no endpoint is
  either client-side, behind a wall you did not reach, or vapour. Say which.
- Every endpoint → which feature? An endpoint serving no known feature is a discovery —
  chase it. This is where undocumented capability shows up.
- Every domain rule that must run somewhere → is it client-side or server-side? If a
  computation's inputs go up and only the result comes back, **the engine is server-side and
  you cannot observe it** — that is a first-order finding for Stage 5 and for the estimate.

### 5. Generate the client

Emit a typed client (TypeScript by default) covering every endpoint.

- `OBSERVED` + `called` → real implementation, types from actual response bodies.
- `OBSERVED` + not called, or `INFERRED` → **stub that compiles and returns a typed fixture,
  with `// UNVERIFIED:` on the line.** It must be impossible to use one by accident and
  think it is real.
- Types come from the actual samples, not from your idea of what the shape should be. Where
  samples conflict across calls, the type is a union and that fact is a finding.

Tooling is optional and secondary — `reverse-api-engineer` (HAR→client) and `Integuru`
(chained request graphs) exist and can save time, but the contract above is the deliverable
whether or not you use them. Do not let a tool's output become the spec unreviewed.

### 6. Security pass

Log a `SEC` finding for: endpoints returning data with no auth, missing authorization checks
(an id you can change that returns someone else's shape — **note the shape, do not harvest
the data**), PII in responses beyond what the screen shows, verbose errors leaking internals,
open GraphQL introspection, secrets in bundles, absent rate limiting. Severity + anchor.
Report. Never weaponise.

---

## Proof requirements

- An endpoint is `OBSERVED` only if it appears in the HAR or as a literal string in a saved
  bundle. Anchor every one.
- Request/response shapes cite the specific HAR entry and JSON path
  (`har:recon/traffic.har#412$.data.holdings[0].isin`).
- Endpoints reasoned from feature names and REST convention are `INFERRED` with a `basis`.
  They are hypotheses. Label them as such in the client, in the manifest, and in the doc.
- **`api.live` is `true` only if the client hits real, verified endpoints.** If any part is
  stubbed, it is `false`, and the per-endpoint `verified` flag carries the detail.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/api/endpoints.md` | The per-endpoint contracts (step 2) |
| `blueprint-out/api/auth-model.md` | Auth sequence, token claims, roles, tenancy |
| `blueprint-out/api/flows.md` | Multi-step chained operations |
| `blueprint-out/api/conventions.md` | Errors, pagination, versioning, naming |
| `blueprint-out/api/client.ts` | Typed client, unverified methods marked |
| `blueprint-out/api/openapi.json` | If derivable — useful downstream |
| `blueprint-out/evidence/ledger.jsonl` | Append `API-*` and `SEC-*` |

Manifest slice `api`:
```jsonc
"api": {
  "endpoints_doc":"blueprint-out/api/endpoints.md", "client_path":"blueprint-out/api/client.ts",
  "language":"typescript", "live": false,
  "endpoints":[{"id":"API-014","method":"POST","path":"/v2/holdings/import","feature":"F-IMP-03",
                "auth":"bearer","grade":"OBSERVED","called":true,"verified":true,
                "async":true,"anchors":["har:recon/traffic.har#412"]}],
  "counts":{"observed_called":41,"observed_uncalled":17,"inferred":9},
  "auth":{"scheme":"jwt","refresh":true,"tenancy_claim":"org_id","claim":"API-002"},
  "pagination":{"style":"cursor","cursor_decodes_to":"base64({sort_key, last_id})","claim":"API-051"},
  "server_side_engines":["gains-computation"],
  "security_findings":["SEC-004","SEC-007"]
}
```
Then `status.api = "done"`.

`pagination.cursor_decodes_to`, `auth.tenancy_claim` and `server_side_engines` are the
fields Stage 4 and Stage 5 depend on most. Fill them.

---

## Done when

- [ ] Every HAR request accounted for (grouped into endpoints, statics excluded)
- [ ] Bundles mined; uncalled endpoints listed with `called: false`
- [ ] Every endpoint has request + success + **error** shapes
- [ ] Auth sequence documented end to end; JWT claims recorded, token value never written
- [ ] Pagination style per collection; cursors decoded
- [ ] Multi-step flows documented as sequences
- [ ] Feature↔endpoint reconciliation complete, both directions
- [ ] Server-side-only computations identified and named for Stage 5
- [ ] Client compiles; every unverified method marked
- [ ] Ledger self-check passes

---

## Never

- Never present an inferred endpoint as observed, in the doc, the manifest, or the client.
- Never invent a request or response field. If a field appeared in one sample and not
  another, that is the finding — write it down.
- Never call `api.live = true` when any part is stubbed.
- Never write a real token, cookie or credential into any artifact.
- Never probe for vulnerabilities beyond what passive observation reveals, and never harvest
  another user's data to demonstrate an exposure. One shape is proof enough.
