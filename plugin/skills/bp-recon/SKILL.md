---
name: bp-recon
description: Stage 2 — evidence capture. Drives a browser through the target guided by the domain hunt list and the intel feature inventory, and saves every artifact later stages need as proof - screenshots, full network capture, DOM, JS bundles and source maps, response headers, client storage, and ID/pagination samples. Capture is the ONLY stage that can produce OBSERVED evidence; everything downstream is limited by what you save here.
---
# bp-recon — capture the proof

## Your job

You are the only stage that can create `OBSERVED` evidence. Every other stage is
reasoning over what you saved. **If you do not save it, it does not exist.**

Two things separate this from a crawl:

1. **You crawl with a list.** `blueprint-out/domain/hunt-list.md` and
   `blueprint-out/intel/features.md` tell you what must exist. You go find those specific
   things. A crawler that follows nav links finds the marketing site; you are looking for
   the import flow, the error state, the recompute button, the settings that reveal the
   data model.
2. **You capture forensics, not pictures.** Screenshots are the least valuable thing you
   collect. The valuable things are the network capture, the JS bundles, the response
   headers, and the ID formats — because those are what let Stage 3 and Stage 4 prove
   claims about the API and the database.

## Load first

- **`bp-mandate`** — read it first. This stage is where hesitation does the most damage.
  Recording your own browser's traffic and reading the JS the server sent you is the
  job — not a grey area. Do it.
- `bp-manifest`, `bp-evidence` (your prefix is `REC`; security findings use `SEC`)
- `blueprint-out/domain/hunt-list.md` — **this is your task list.** Work it item by item.
- `blueprint-out/intel/features.md` — every feature is a thing to go find and exercise.
- `blueprint-out/intel/demos.md` — videos show you where things live. Watch/read before you
  crawl; it saves enormous time.
- From the manifest: `target.url`, `target.extra_urls`, `target.auth`.

## Requirements

A browser tool: a Playwright/Chrome MCP, or Node + Playwright for the bundled
`recon.mjs`. **Without a browser, stop and say so.** You cannot infer your way through
this stage — that would produce the exact fabrication the whole pipeline exists to prevent.

---

## What you are cleared to do

Authorization was settled at intake. Do not ask again. **Go and capture.**

You are cleared to, without asking: crawl every route you can reach, screenshot everything,
record all network traffic, submit forms with test data, **deliberately submit bad data to
capture validation errors**, download and read every JS bundle and source map, read
localStorage and cookies, decode a JWT to read its claims, call public endpoints and record
what they return, check whether GraphQL introspection is enabled, and — with the credentials
the user supplied — log in and do all of it again inside the app.

Four things stop a specific action (see `bp-mandate` §3). Nothing else does:

1. **Do not attack** — no exploiting, brute-forcing, fuzzing, or abusive request rates.
   Insert delays. Honour robots.txt. You are one visitor, not a load test.
2. **Do not take other people's data** — if an id swap exposes another user's record, save
   **one** redacted example of the *shape*, log a `SEC` finding, and stop. Never enumerate.
3. **Do not bypass a wall** — no credentials means those routes are `behind-auth`. Record
   that and move on; it is a finding, not a blocker.
4. **Do not leak secrets** — credentials, cookies and bearer tokens never get written to
   `blueprint-out/`. Scrub `Authorization`, `Cookie` and `Set-Cookie` **values**; keep the
   header *names* and the token *shape* (`Bearer <JWT, 3 segments, alg=RS256>` is useful
   evidence; the token itself is a liability). `recon.mjs` does this automatically — if you
   capture by hand, do it yourself.

If `target.auth.authorized` is not set, you work the public surface only. That is a smaller
run, not a cancelled one — capture everything public and say clearly what a login would add.

---

## Method

### 1. Mechanical sweep first

Run the bundled capture script to get the baseline. It handles the tedious part.

```bash
node recon.mjs --url "$TARGET_URL" --out blueprint-out/recon \
  ${AUTHORIZED:+--har} ${LOGIN_URL:+--login "$LOGIN_URL"}
```

It writes: `shots/`, `dom/`, `traffic.har`, `bundles/`, `headers.json`, `storage/`,
`console.log`, `recon.json`. Read `recon.json` when it finishes.

If you have a browser MCP instead, do the same by hand: navigate, screenshot full page,
dump `page.content()`, record network, fetch every same-origin `.js`, dump storage.

### 2. Route discovery — go past the nav

Nav links are the shallow surface. Also pull routes from:
- `sitemap.xml`, `sitemap_index.xml`, `robots.txt` (both its `Sitemap:` lines *and* its
  `Disallow:` lines — disallowed paths are a map of what they consider interesting)
- `__NEXT_DATA__`, `window.__INITIAL_STATE__`, `__NUXT__`, other hydration blobs in the HTML
- **the JS bundle's route table** — SPA routers ship their full route list in the bundle.
  Grep for route arrays, `path:` keys, lazy-import maps. This routinely reveals screens
  that no link points to.
- link rel=alternate/canonical, OpenAPI/Swagger at `/openapi.json`, `/swagger.json`,
  `/api-docs`, `/v1/openapi`, GraphQL at `/graphql`
- `.well-known/`, `/config`, `/api/config`, `/env.json` — config endpoints leak field shapes
- the app subdomain. If the marketing site is `example.com`, the product is probably at
  `app.example.com` or `my.example.com`. **Check.** Crawling only the marketing site is the
  single most common way this stage fails.

### 3. Exercise features, don't just visit pages

A screenshot of a form proves the form exists. **Submitting the form proves what the API
does.** For every feature in `features.md` that you can reach:

- Trigger it. Fill the form with valid data, submit, capture the request and response.
- Then trigger it **wrong** — empty required field, bad format, out-of-range value, too-large
  file. **Validation errors are the highest-value capture in this entire stage**: the error
  response tells you field names, types, constraints, and often the exact DB column rules.
  This is how you recover a schema you were never shown.
- Capture every state the feature can be in: empty (new account, no data), loading, partial,
  success, each error. `bp-ux` needs these; nobody else can get them.
- Paginate. Sort. Filter. Each one is a query parameter that reveals an index.
- If there is a "recompute", "refresh", "sync", or "recalculate" action — **use it and watch
  the network.** Whether results are computed on demand or read from storage is a
  first-order architecture fact.

### 4. Capture what Stage 4 needs to identify the database

`bp-datastore` has to figure out what they actually store data in. It can only do that from
what you save. Explicitly collect:

| Signal | Where to get it | Save to |
|---|---|---|
| **ID formats** | Any entity id in any response. Note the shape exactly: 24-hex (Mongo ObjectId), UUIDv4, ULID/KSUID, sequential int, Snowflake-like int64, base64 opaque. Collect **many samples of the same entity type** — sequence gaps tell you if it is an auto-increment. | `recon/samples/ids.json` |
| **Pagination style** | List endpoints. Offset+limit vs opaque cursor vs `startAfter`. Decode base64 cursors — they frequently contain the sort key and the underlying id. | `recon/samples/pagination.json` |
| **Response headers** | Every response. `Server`, `X-Powered-By`, `x-amz-*`, `x-goog-*`, `x-azure-*`, `cf-ray`, `x-vercel-*`, `x-request-id` format, cache headers. | `recon/headers.json` |
| **Error bodies** | Deliberate bad requests. Driver names, constraint names, and stack fragments leak here. | `recon/samples/errors.json` |
| **Timestamp formats** | Any dated field. ISO-8601 with `Z` vs epoch millis vs epoch seconds vs Mongo `$date`. Precision (seconds/millis/micros) hints at the column type. | in `samples/` |
| **Nesting shape** | Whether a "detail" response embeds children or requires a second call. | in `samples/` |
| **Client storage** | `localStorage`, `sessionStorage`, IndexedDB names, cookie names and flags. Feature flags and cached entities live here. | `recon/storage/` |

Save **raw response bodies** for at least one call per endpoint into
`recon/samples/responses/` — Stage 3 and Stage 4 need to re-read the actual JSON, not your
summary of it.

### 5. Mine the bundles (authorized targets)

The shipped JavaScript is the product's source code with the names removed. Fetch every
same-origin `.js` and any `.map` files, save them, then grep for:

- **API base URLs and endpoint strings** — `/api/v`, `fetch(`, `axios.`, template literals
  with paths. This finds endpoints the UI never calls in your session.
- **GraphQL documents** — full queries/mutations with their exact field selections. This is
  a schema fragment handed to you.
- **Route tables** — the full screen list, including admin/internal routes.
- **Feature flags** — flag names tell you what is being built and what is gated.
- **Validation schemas** — zod/yup/joi objects shipped to the client are **literally the
  field definitions with types and constraints**. If you find these, Stage 4's job is
  half done. Search for `.string()`, `.required()`, `min(`, `max(`, `regex(`.
- **Enums and constants** — status values, type codes, category lists. These are DB enum
  columns.
- **Accidentally shipped secrets** — API keys, tokens, internal URLs. These are `SEC`
  findings: **report them, never use them.**
- If `.map` source maps are present, reconstruct the original file tree. Directory names
  reveal the service architecture.

### 6. Probe the unauthenticated surface (report, don't exploit)

Identify endpoints that return data without auth. Take note as both a coverage win and a
`SEC` finding with severity. Check GraphQL introspection — if enabled, capture the schema
(that is the complete type system, the single richest artifact available).

**Boundary:** requesting a public URL and recording that it returned data is observation.
Iterating ids to pull other users' records is not. Stop at the first record that proves the
exposure, note it, move on.

### 7. Authenticated pass (if credentialed)

Log in and **redo steps 3–5 inside the app**. This is where the real product lives —
roughly ten times the usable output of an unauthenticated run. Capture the auth flow itself:
login request/response, token type and shape, refresh mechanism, session vs JWT, decoded JWT
*claims* (not the token), role/permission fields, tenancy identifiers.

### 8. Work the hunt list and close it out

Go through `hunt-list.md` item by item. Mark each ✅ found (with anchor) / ❌ not found
(with what you tried) / 🔒 behind a wall you cannot pass.

**❌ items are findings, not failures.** "The domain requires corporate-action handling and
there is no screen for it anywhere in the product" is one of the most valuable sentences the
whole run can produce. Write it down and hand it to Stage 6.

---

## Proof requirements

- Everything you claim from this stage is `OBSERVED` and carries a real anchor into a file
  you actually wrote (see `bp-evidence` for anchor formats). No exceptions — you had the
  browser open; there is no excuse for an unanchored recon claim.
- The screen inventory records, per route: reached / behind-auth / not-found / blocked, and
  which artifacts exist for it.
- Every `SEC` finding: what is exposed, the anchor, severity, and **no exploitation**.

---

## Emit

```
blueprint-out/recon/
  recon.json            # machine summary written by recon.mjs
  shots/                # full-page screenshots per route + per state
  dom/                  # rendered DOM per route
  traffic.har           # full network capture (authorized runs) — secrets scrubbed
  bundles/              # every same-origin .js and .map
  headers.json          # response headers per endpoint
  storage/              # localStorage / sessionStorage / cookie names / IndexedDB names
  samples/
    responses/          # raw response bodies, one+ per endpoint
    ids.json            # id format samples per entity
    pagination.json     # pagination style per list endpoint
    errors.json         # validation/error responses
  console.log
  coverage.md           # screen inventory + hunt-list close-out
  findings-security.md  # SEC findings with severity
```

Manifest slice `recon`:
```jsonc
"recon": {
  "shots_dir":"blueprint-out/recon/shots", "dom_dir":"blueprint-out/recon/dom",
  "har":"blueprint-out/recon/traffic.har", "bundles_dir":"blueprint-out/recon/bundles",
  "samples_dir":"blueprint-out/recon/samples", "coverage":"blueprint-out/recon/coverage.md",
  "routes":[{"url":"...","status":"reached|behind-auth|not-found|blocked","shot":"...","dom":"..."}],
  "authenticated": true,
  "hunt_list_closed": {"found":18,"not_found":4,"blocked":2},
  "endpoints_seen": 63,
  "bundle_findings": {"routes_from_bundle":31,"graphql_docs":12,"validation_schemas":8,"flags":14},
  "security_findings": [{"id":"SEC-002","title":"...","severity":"medium","anchor":"..."}]
}
```
Then `status.recon = "done"`.

---

## Done when

- [ ] The **app** subdomain was crawled, not just the marketing site
- [ ] Every hunt-list item marked ✅/❌/🔒 with evidence or an explanation
- [ ] Every reachable feature in `features.md` was *exercised*, not just viewed
- [ ] Deliberate validation errors captured for every form you could submit
- [ ] Every feature's states captured (empty/loading/partial/success/errors)
- [ ] Raw response bodies saved for every endpoint seen
- [ ] `samples/ids.json` + `pagination.json` + `errors.json` + `headers.json` populated
- [ ] Bundles fetched and mined; route table, GraphQL docs, validation schemas extracted
- [ ] Auth flow mapped (if credentialed); tokens scrubbed everywhere
- [ ] No credential, cookie value, or bearer token appears anywhere in `blueprint-out/`
- [ ] `coverage.md` states honestly what was NOT reached and why
- [ ] Ledger self-check passes

---

## Never

- Never crawl only the public marketing site and call the stage done.
- Never write a screenshot-only capture. Pictures without traffic make Stage 3 and 4 guess.
- Never save a real credential, session cookie, or bearer token to disk.
- Never exploit a vulnerability, enumerate other users' data, bypass auth or a paywall, or
  fuzz. Observe, record, report.
- Never claim a screen exists because a doc mentioned it. If you did not reach it, it is
  `behind-auth` or `not-found`, and that is the finding.
- Never let the crawler's 40-route limit silently truncate a bigger app. If you hit the cap,
  say so in `coverage.md` and raise it.
