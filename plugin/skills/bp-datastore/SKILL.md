---
name: bp-datastore
description: Stage 4 — work out what they actually store data in, and in what shape. Identifies the real database technology from public engineering evidence (job postings, subprocessor lists, status pages, conference talks, response headers, ID formats, pagination style), then reconstructs the schema by inspecting every API request and response and mapping fields back to tables or collections, reasoned against the domain, the user base and the scale. The schema is reconstructed from API traffic, not from screenshots — screens show only the shape of the reports.
---
# bp-datastore — what they store, where, and why

## Your job

Two questions. Answer both with evidence.

1. **What technology are they storing data in?** SQL or NoSQL? Which engine? Managed cloud
   or self-hosted? What supporting stores — cache, search, queue, blob, warehouse?
2. **What is the schema?** Every table or collection, every field, every relationship, every
   index — reconstructed from what the API actually sends and receives.

Then a third, which is what makes this useful: **what should *we* use, given the domain, the
users and the scale?** Their choice is evidence, not gospel. They may have chosen badly, or
chosen well for constraints you do not share.

**Do not derive the schema from screenshots.** Screens show outputs. Everything computed,
intermediate, historical, or audit-related never appears on a screen and is invisible to
that method. You work from the API and from the domain.

## Scope — do only this

- **Deliver:** the named storage technology (with a confidence level) and the reconstructed
  schema as a graph, plus what *we* should use.
- **Do not:** re-observe the product or reverse the engines. You reason over `api` and
  `recon/samples/` — you do not open the browser again. Whether a value is computed by an
  engine is a fact you record; *how* it is computed is `engines`' job.
- **Emit:** the files under `## Emit`, the `datastore` slice, and `DS-*` ledger lines.
- **Stop when:** the technology is named with a signal table behind it, and every schema field
  traces to a sample, a request, a validation schema, an error, or a stated domain inference.
  "Some modern datastore" does not close this stage; a named engine with `confidence: low`
  does.

## Load first

- **`bp-mandate`** — read it first. Everything here comes from public sources and from
  traffic your own browser made. Reading a company's careers page is not espionage. Work.
- `bp-manifest`, `bp-evidence` (your prefix is `DS`)
- `blueprint-out/api/endpoints.md`, `conventions.md`, `auth-model.md` — your primary input
- `blueprint-out/recon/samples/` — **the raw response bodies, ids, pagination, errors.
  Read the actual JSON files.** Not a summary of them.
- `blueprint-out/recon/headers.json`, `bundles/`, `storage/`
- `blueprint-out/intel/` — especially `tech_signals`, which Stage 1 collected for you
- `blueprint-out/domain/domain-brief.md` — retention, audit, immutability and consistency
  requirements are **architectural** and decide storage choices

---

## PART A — Identify the technology

Run all six methods. Each produces evidence. Then weigh them together.

### A1. Public engineering evidence (search for this — it is usually decisive)

Companies tell you their stack in public, constantly. Go look:

| Source | Search / where | What it gives |
|---|---|---|
| **Job postings** | `"<company>" careers backend engineer`, LinkedIn Jobs, their `/careers` page | The single best source. Backend roles list the actual stack: "PostgreSQL, Redis, Kafka, Elasticsearch". Save the posting text. |
| **Trust / security page, subprocessor list** | `<domain>/security`, `/trust`, `/legal/subprocessors`, `/gdpr` | **Legally required to be accurate.** Names the cloud provider and often the exact managed database (Amazon RDS, MongoDB Atlas, Google Cloud SQL, Snowflake). |
| **Engineering blog** | `<company> engineering blog`, `<company>.com/blog/engineering`, Medium | "How we scaled X" posts name the database and the problem it solved. |
| **Conference talks & podcasts** | `"<company>" site:youtube.com engineering architecture`, meetup listings | Engineers describe the architecture on stage. |
| **Vendor case studies** | `"<company>" site:mongodb.com`, `site:aws.amazon.com/solutions/case-studies`, `site:planetscale.com`, `site:elastic.co`, `site:snowflake.com`, `site:redis.com`, `site:cockroachlabs.com` | **Check whether the company is a named customer or partner of a database vendor.** A vendor case study is a signed, on-the-record statement of what they run. Highest-grade evidence available short of a leak. |
| **StackShare / BuiltWith / Wappalyzer** | Search the company | Crowd-sourced; treat as a lead to verify, not proof. |
| **GitHub** | The company's org; any open-source repo, SDK, or Terraform | Dependency files (`package.json`, `requirements.txt`, `go.mod`, `Gemfile`) name database drivers directly. |
| **Status page** | `status.<domain>` | Component names ("Database", "Search cluster", "Async workers") map the architecture. Incident write-ups often name the technology. |
| **Patent / regulatory filings** | For larger or regulated companies | Sometimes describe the system in detail. |

`bp-intel` already put anything it found into `intel.tech_signals`. Start there, then search
for the rest yourself.

### A2. Response header fingerprints

From `recon/headers.json`:

| Header pattern | Tells you |
|---|---|
| `x-amz-*`, `x-amzn-*`, `x-amz-cf-id` | AWS (CloudFront / API Gateway / ALB) |
| `x-goog-*`, `x-cloud-trace-context` | Google Cloud |
| `x-azure-ref`, `x-ms-*` | Azure |
| `cf-ray`, `cf-cache-status` | Cloudflare in front |
| `x-vercel-id`, `x-nf-request-id`, `fly-request-id` | Vercel / Netlify / Fly |
| `Server: gunicorn\|puma\|Kestrel\|Express\|nginx` | Application runtime → narrows the ORM → narrows the DB |
| `x-powered-by` | Framework, when they forgot to disable it |
| `x-request-id` **format** | A UUID vs a Snowflake vs a ULID hints at the id strategy used internally too |

Cloud provider narrows the likely managed database set. It is a prior, not a conclusion.

### A3. ID format — the strongest single technical signal

From `recon/samples/ids.json`. Read actual id values:

| Observed id | Almost certainly |
|---|---|
| 24 lowercase hex chars (`507f1f77bcf86cd799439011`) | **MongoDB ObjectId.** Near-conclusive. |
| Sequential integers, small gaps, monotonic across a page | **Relational auto-increment / identity column.** Postgres or MySQL. |
| UUID v4 (random) | Relational or document; app-generated. Common with Postgres `uuid` columns. |
| UUID v7 / ULID / KSUID (time-sortable prefix) | Modern app-generated, usually relational, chosen for index locality |
| Large int64, non-sequential, time-ordered | Snowflake-style distributed id — a sharded or distributed store |
| `prefix_alphanumeric` (`cus_9s8d7f`) | Stripe-style external id; the internal key is separate and hidden |
| Composite `tenant#entity#id` | **Single-table DynamoDB or another key-value store.** Look for `pk`/`sk` field names. |
| Base64/opaque | Encoded — decode it, it usually contains one of the above |

**Collect many samples of the same entity.** One id tells you the format; twenty tell you
whether it is sequential, and sequential-vs-random is the fork between relational and
document thinking.

### A4. Query semantics — how they page and filter reveals the engine

From `recon/samples/pagination.json` and the endpoint query parameters:

- **`?offset=&limit=`** → relational thinking, `LIMIT/OFFSET`. Very common with SQL ORMs.
- **Opaque cursor** → keyset pagination. **Decode it** (usually base64 JSON): it typically
  contains the sort field and the last id, which hands you the primary index directly.
- **`startAfter` / `pageToken` / `LastEvaluatedKey`** → Firestore / GCP / DynamoDB.
- **`_scroll_id`, `search_after`, `took` in the response, `_source`/`highlight` fields, a
  `total.relation: "gte"`** → **Elasticsearch or OpenSearch** behind a search endpoint.
- **Every filterable query parameter is an index.** Write them all down — they become the
  index list in your schema.
- **`__typename`, `edges`/`node`/`pageInfo`** → GraphQL with Relay conventions; says nothing
  about the store, so keep digging.
- **Deeply nested single response vs many small calls** → embedded document model vs
  normalised relational + joins. Strong signal.
- **Repeated denormalised blocks** (the same author object embedded in fifty posts) →
  document store, or a deliberate read-model cache.

### A5. Error and validation leakage

From `recon/samples/errors.json` — the deliberate bad requests recon made:

- Constraint names: `users_email_key`, `UNIQUE constraint failed`, `duplicate key value
  violates unique constraint` → **PostgreSQL**, and you just learned a table name and a
  unique index.
- `ER_DUP_ENTRY`, `Data too long for column 'x'` → **MySQL/MariaDB**, plus a column width.
- `E11000 duplicate key error collection: app.users index: email_1` → **MongoDB**, plus the
  database name, collection name and index name. This one line is worth an hour of guessing.
- `ValidationError` shapes from Mongoose / Sequelize / Prisma / Django / ActiveRecord each
  have a recognisable envelope → identifies the ORM → narrows the DB.
- Field-level validation messages give you types, lengths, formats and nullability.

### A6. Shipped client-side validation schemas

From `recon/bundles/`. If the frontend ships zod / yup / joi / class-validator objects,
those are **the field definitions with types and constraints**, written by the same team,
usually mirroring the server model. Grep for `.string()`, `.number()`, `.optional()`,
`.min(`, `.max(`, `.email()`, `.uuid()`, `.enum([`. Extract them wholesale.

Also grep the bundles for driver and service names that leaked into client code: `mongodb`,
`postgres`, `redis`, `algolia`, `elasticsearch`, `firebase`, `supabase`, `amplify`,
`dynamodb`, `pusher`, `ably`. A Firebase or Supabase config object in the client is a
complete answer — those talk to the database directly from the browser.

### A7. Weigh it up and commit

Build a table of every signal, its source, its anchor, and what it points to. Then state a
conclusion with a confidence level:

```markdown
| # | Signal | Points to | Grade | Anchor |
|---|---|---|---|---|
| 1 | Careers page: "strong PostgreSQL, Redis" | Postgres + Redis | EXTERNAL | INT-031 |
| 2 | Subprocessor list names Amazon RDS | Managed Postgres/MySQL on AWS | DOCUMENTED | DS-004 |
| 3 | Sequential integer ids, no gaps over 40 rows | Relational auto-increment | OBSERVED | DS-006 |
| 4 | `offset`/`limit` pagination throughout | SQL ORM | OBSERVED | DS-007 |
| 5 | Error: `users_email_key` unique violation | **PostgreSQL** + table `users` | OBSERVED | DS-009 |
| 6 | `x-amz-cf-id` on all responses | AWS | OBSERVED | DS-002 |

**Conclusion:** primary transactional store is **PostgreSQL on Amazon RDS**.
Confidence: **high** — five independent signals agree, and #5 is a Postgres-specific
error string, which is close to conclusive.
```

**Commit to an answer.** "It could be any database" is not a finding. Weigh the evidence,
name the most likely technology, state your confidence, and list what would confirm or
refute it. If the evidence genuinely splits, say which two candidates and what would
distinguish them.

### A8. Map the supporting stores

The primary database is never the whole picture. Look for evidence of each:

| Store | Evidence to look for |
|---|---|
| **Cache** | Very fast repeat responses, `x-cache` headers, "Redis"/"Memcached" in postings, cache-invalidation endpoints |
| **Search** | A separate `/search` endpoint with different response shape, relevance scores, highlighting, typo tolerance, faceting |
| **Queue / async** | Endpoints returning a job id + a poll endpoint; "Kafka"/"SQS"/"Celery"/"Sidekiq" in postings; delayed side effects |
| **Blob / object storage** | Presigned upload URLs, S3/GCS/Azure hostnames in responses |
| **Analytics / warehouse** | Reporting endpoints that are slow, aggregate-only, and lag live data; "Snowflake"/"BigQuery"/"Redshift" in postings |
| **Time-series** | Metric/chart endpoints with fixed bucket intervals and downsampling |
| **CDN / edge** | Covered by headers |

---

## PART B — Reconstruct the schema

### B1. Entities from responses

For every response body in `recon/samples/responses/`:
1. Every distinct object shape is a candidate entity.
2. Every field: name, JSON type, nullability **across all samples** (a field null in some
   and populated in others is optional or conditional — record which).
3. Note formats precisely: dates (ISO-8601 vs epoch, and the precision), decimals (string vs
   float — **money as a float is a defect and money as a string means they got it right**),
   enums (collect every value seen).
4. Nested objects → either an embedded document or a joined relation. Decide using A4's
   nesting signal and record your reasoning.
5. Arrays of objects → one-to-many. Arrays of ids → many-to-many with a join table.

### B2. Fields the API never returns — reason them in

This is the part screenshot-based methods cannot do, and it is most of the real schema.

- **Write-only fields** — anything in a request body that never comes back (passwords,
  internal flags, raw uploads).
- **Audit columns** — `created_at`, `updated_at`, `created_by`, `deleted_at`. If any appears
  anywhere, assume the pattern is applied across the schema and say so.
- **Soft deletes** — a "restore" or "trash" feature means `deleted_at`, not a hard delete.
- **Intermediate state** — a multi-step flow (import → review → commit) must persist the
  in-between state somewhere. That is a table nobody ever renders.
- **Job/task tables** — every async endpoint implies a jobs table with status, attempts,
  error, timestamps.
- **Audit / event log** — if the domain brief requires reconstructibility or retention
  [cite the `DOM` claim], there is an append-only table. Its absence would be a compliance
  finding.
- **Tenancy columns** — from `api.auth.tenancy_claim`. If the JWT carries `org_id`, then
  `org_id` is on nearly every table, and it is the first column of nearly every index.
- **Computed vs stored** — if a "recompute" action exists, results are probably derived, not
  stored. If a historical value never changes after the fact, it is stored (snapshotted).
  **Get this right — it is the single biggest schema decision in most products**, and it
  decides whether the engines run on read or on write.
- **Derived read models** — heavy dashboards that load instantly are reading a rollup table
  or a materialised view, not aggregating live.

### B3. Model the schema as a GRAPH, not a list of tables

A list of tables is not a data model. The model IS the graph — the entities are nodes, the
relationships are edges, and the product's behaviour lives in the edges. Go to graph depth.

**Build the entity graph explicitly.** Every node and every edge gets specified:

- **Nodes** — one per entity. Record: primary key, natural key (the business-unique field,
  e.g. `isin` or `email`), tenancy column, and whether it is a *strong* entity (exists on its
  own) or *weak* (only exists as a child — a line item, an allocation, an audit row).
- **Edges** — one per relationship, and each edge is fully typed:
  - **Cardinality** — `1:1`, `1:N`, `N:M`. Never leave it implied.
  - **Direction & ownership** — which side holds the foreign key; which side is the parent.
  - **Optionality** — is the FK nullable? A nullable FK is a real modelling decision, not an
    accident (an order with no assigned agent yet vs. one that must always have a customer).
  - **On-delete behaviour** — cascade, restrict, set-null, or soft (the parent's `deleted_at`
    logically orphans children). Get this from the product's delete/restore behaviour.
  - **Evidence** — the anchor: the response where the child embedded the parent, the
    `?parent_id=` filter, the FK-shaped field, or the join you inferred and why.
  - **N:M edges become their own node** — the join table. Name it, and check whether it
    carries its own fields (a `membership` row with a `role` and `joined_at` is an entity,
    not just a link). Join tables with attributes are where half the real schema hides.

**Resolve these graph properties — they are what a flat list misses:**

1. **Cycles.** Self-references (`Category.parent_id → Category`, `Employee.manager_id`) and
   mutual references (`User.default_org` ↔ `Org.owner`). Each cycle needs a nullable edge or
   a bootstrap order, or inserts deadlock. Flag every one.
2. **Hierarchies.** Any self-referential N-level tree (org units, categories, threaded
   comments, account trees). Name the pattern you'd use — adjacency list, closed-loop, or
   materialised path — and justify it from the read patterns you observed (deep reads →
   closure table; shallow → adjacency list).
3. **Polymorphic edges.** A `comment` or `attachment` or `audit_log` that points at *many*
   entity types (`target_type` + `target_id` in the response). Call it out — it's a common
   shape and it breaks naive FK modelling.
4. **Fan-in hubs.** The one or two nodes almost every other node points at — usually `user`,
   `org`/`tenant`, `account`. These are your index-first, shard-key, and access-control
   anchors. Mark them; the whole system's scale story runs through them.
5. **Ordering.** Any edge whose children have a user-visible order (line items, playlist
   tracks, kanban cards) needs a `position`/`rank` field. If you saw drag-to-reorder, it's
   there. Naive schemas forget it and break.
6. **Temporal edges.** Relationships that change over time and must keep history (a holding's
   ownership, a price, an assignment). These aren't one edge — they're an edge *table* with
   `valid_from`/`valid_to`. The domain brief's retention rules decide which edges are temporal.

**Emit the graph in two forms:**

- **`er.mmd`** — Mermaid `erDiagram` with every entity, every field with its type and key
  marker (`PK`/`FK`/`UK`), and every relationship rendered with **crow's-foot cardinality and
  optionality** (`||--o{`, `}o--o{`, etc.). Not a box-and-line sketch — a real ER diagram
  where the notation carries the cardinality. Split into one diagram per bounded context if
  the whole graph exceeds ~20 nodes (one unreadable diagram helps no one).
- **`graph.json`** — the machine-readable model, so later stages and tools can traverse it:

```jsonc
{
  "nodes": [
    {"id":"holding","pk":"id","natural_key":"isin+account_id","tenancy":"org_id",
     "kind":"strong","fields":24,"claim":"DS-021"}
  ],
  "edges": [
    {"from":"holding","to":"account","type":"N:1","fk_on":"holding.account_id",
     "optional":false,"on_delete":"restrict","evidence":"observed",
     "anchor":"har:recon/traffic.har#288$.account_id","claim":"DS-030"}
  ],
  "cycles":[["user","org","user"]],
  "hierarchies":[{"node":"category","pattern":"closure-table","reason":"deep-read dashboard [DS-041]"}],
  "polymorphic":[{"node":"audit_log","targets":["holding","trade","import"],"disc":"target_type"}],
  "hubs":[{"node":"org","fan_in":27},{"node":"user","fan_in":19}],
  "temporal_edges":[{"edge":"holding→owner","reason":"retention [DOM-052]"}]
}
```

Grade every edge `observed` (FK seen in a response, or a `?parent_id=` filter) vs `inferred`
(named it from convention + domain). A relationship is a claim like any other — anchor it.

### B4. Indexes from observed queries and from the graph

Every filter, sort and search parameter you saw is an index. Every unique-constraint error is
a unique index. Every pagination cursor names its sort key. Compose them: a filter on `org_id`
plus a sort on `created_at` is a composite index `(org_id, created_at DESC)`.

**Then derive the edge indexes the graph demands** — every FK you plotted needs an index on
the child side for the join to be cheap; every fan-in hub needs its inbound FKs indexed; every
temporal edge needs `(entity_id, valid_to)`. List each with the observation or the edge that
implies it.

### B5. Reason from domain, users and scale

Now step back and sanity-check the reconstruction against reality. Estimate, and show your
working:

- **Users** — from pricing, reviews, funding, employee count, "trusted by N" claims, app
  store install counts. Order of magnitude is enough.
- **Data volume** — users × records per user × record size. A tax product holding ten years
  of transactions per user is a very different problem from a to-do app.
- **Read/write mix** — most products are read-heavy; import/batch products are not.
- **Peak vs average** — domains have seasons. A tax product's peak is the fortnight before
  the filing deadline and may be 100× the mean. **Size for the peak.**
- **Consistency needs** — money and compliance need strong consistency and transactions.
  Feeds and analytics tolerate eventual consistency. This constrains the engine choice more
  than scale does.
- **Retention and audit** — from the domain brief. Long retention plus immutability plus
  reconstructibility means an append-only ledger and probably an archival tier.
- **Multi-tenancy** — shared schema with a tenant column (usual), schema-per-tenant, or
  database-per-tenant (enterprise/regulated). Evidence: the JWT claim, URL structure, and
  whether enterprise plans promise isolation.

Then answer: **does the technology in Part A make sense for this?** If they run MongoDB for
a system requiring multi-entity financial transactions, say so — that is a genuine finding
about their engineering, and it feeds `bp-gaps`.

### B6. Recommend our store

Separate section, clearly labelled as recommendation not observation. Given the domain,
scale, consistency and compliance constraints: what should we use, and why? Where we differ
from them, justify it. Where we match them, say that too — matching a proven choice is a
good decision, not a lack of one.

---

## Proof requirements

- Every technology claim carries its signal table row + anchor. **A database named with no
  evidence row is a guess and must be labelled `INFERRED` with `confidence: low`.**
- Every field in the schema traces to a response sample, a request body, a validation
  schema, an error message, or an explicit domain-driven inference with a `basis`.
- Scale estimates are `INFERRED` and must show the arithmetic. "Roughly 50k users" with no
  derivation is worthless; "~50k users (pricing page claims 'over 40,000 investors'
  [INT-012], app store shows 100k+ installs [INT-014], so 40–80k active)" is usable.
- Mark every schema element `observed` / `derived` / `assumed`, and give the counts.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/datastore/technology.md` | Part A: the signal table, the conclusion, confidence, supporting stores |
| `blueprint-out/datastore/schema.prisma` | The reconstructed model (or `schema.sql`, or `collections.md` for document stores) |
| `blueprint-out/datastore/schema.sql` | DDL with indexes and constraints |
| `blueprint-out/datastore/er.mmd` | Crow's-foot ER diagram(s) — cardinality + optionality in the notation, one per bounded context if large |
| `blueprint-out/datastore/graph.json` | The machine-readable entity graph: nodes, typed edges, cycles, hierarchies, polymorphic edges, hubs, temporal edges |
| `blueprint-out/datastore/reasoning.md` | Part B5–B6: scale arithmetic, computed-vs-stored calls, tenancy, our recommendation |
| `blueprint-out/datastore/field-provenance.md` | Every field → where it came from |
| `blueprint-out/evidence/ledger.jsonl` | Append `DS-*` |

Manifest slice `datastore`:
```jsonc
"datastore": {
  "technology": {
    "primary":{"engine":"PostgreSQL","hosting":"Amazon RDS","confidence":"high",
               "signals":["DS-002","DS-004","DS-006","DS-007","DS-009"]},
    "supporting":[{"role":"cache","engine":"Redis","confidence":"medium","signals":["INT-031"]},
                  {"role":"search","engine":"Elasticsearch","confidence":"low","signals":["DS-018"]}],
    "cloud":"AWS"
  },
  "schema_prisma":"blueprint-out/datastore/schema.prisma",
  "er_diagram":"blueprint-out/datastore/er.mmd",
  "graph":"blueprint-out/datastore/graph.json",
  "entities":[{"name":"Holding","fields":24,"source":"observed","claim":"DS-021"}],
  "counts":{"entities":31,"edges":58,"fields_observed":198,"fields_derived":64,"fields_assumed":22},
  "graph_shape":{"cycles":1,"hierarchies":["category"],"polymorphic":["audit_log"],
                 "hubs":[{"node":"org","fan_in":27},{"node":"user","fan_in":19}],
                 "temporal_edges":["holding→owner"]},
  "indexes":[{"table":"holdings","columns":["org_id","created_at"],"reason":"filter+sort on list endpoint","claim":"DS-033"}],
  "computed_not_stored":["portfolio.total_gain"],
  "tenancy":{"model":"shared-schema","column":"org_id","claim":"API-002"},
  "scale_estimate":{"users":"40-80k","peak_multiplier":100,"peak_window":"2 weeks pre-deadline",
                    "data_volume":"~2TB","read_write":"95/5","reasoning_claim":"DS-045"},
  "our_recommendation":{"primary":"PostgreSQL","rationale":"...","differs_from_target":false}
}
```
Then `status.datastore = "done"`.

---

## Done when

- [ ] All six identification methods (A1–A6) actually run, not skipped
- [ ] Searched job postings, subprocessor/trust page, engineering blog, and **checked whether
      the company appears as a named customer in any database vendor's case studies**
- [ ] Signal table built; a technology **named** with an explicit confidence level
- [ ] Supporting stores mapped (cache / search / queue / blob / warehouse) or explicitly ruled out
- [ ] Every entity and field from actual response samples, not from screenshots
- [ ] The invisible schema reasoned in: audit columns, job tables, intermediate state,
      tenancy columns, soft deletes, event log
- [ ] **Schema modelled as a graph** — every entity a node, every relationship a typed edge
      (cardinality, FK side, optionality, on-delete), each graded observed/inferred
- [ ] Cycles, self-referential hierarchies, polymorphic edges, fan-in hubs, ordering fields
      and temporal edges all resolved — not left as an implied flat list
- [ ] `er.mmd` uses crow's-foot notation carrying real cardinality; `graph.json` emitted
- [ ] Computed-vs-stored decided for every derived value, with reasoning
- [ ] Indexes listed, each tied to an observed query OR to an edge/hub/temporal relationship
- [ ] Scale estimated with the arithmetic shown
- [ ] Our recommendation stated and justified
- [ ] Every field's provenance recorded; counts add up
- [ ] Ledger self-check passes

---

## Never

- Never derive the schema from screenshots. Screens show outputs; you need the whole system.
- Never say "some kind of database" or "likely a modern datastore". Name it, grade it, and
  say what would change your mind. Refusing to conclude is not rigour, it is avoidance.
- Never present a technology guess as a finding. Signal table, or `confidence: low`.
- Never skip the public-source search because the technical signals felt sufficient. Job
  postings and subprocessor lists routinely settle in one minute what fingerprinting cannot
  settle at all.
- Never copy their choice without asking whether it fits our constraints — and never
  contradict it without saying why.
- Never hand off a flat table list as the data model. The model is the graph; an edge with no
  cardinality, no FK side and no on-delete is not specified, and the build will guess wrong.
