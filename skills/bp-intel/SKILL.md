---
name: bp-intel
description: Stage 1 — positioning and behavioural feature inventory. Reads everything the vendor and the world have written about the product (docs, pricing, changelog, demos, reviews) and turns it into a feature inventory specified by BEHAVIOUR — trigger, inputs, rules, outputs, states — not by name. A feature list of names is positioning-level and not buildable; behaviour is what a later stage can go verify.
---
# bp-intel — what the product does, behaviourally

## Your job

Two outputs, and the second one is the real one.

1. **Positioning** — what the product claims to be, who it is for, what it charges, and
   why anyone picks it. Short. This frames everything else.
2. **A behavioural feature inventory** — every feature specified precisely enough to
   *build*. Not "has portfolio import". Instead: what triggers it, what it accepts, what
   rules it applies, what it produces, what states it can be in, and what happens when it
   goes wrong.

The difference matters more than anything else in this stage. A feature list of names is a
G2 listing and it is worthless to an engineer. **"Bulk import" is a name. "Accepts a
broker contract-note PDF up to 20MB, password-protected ones prompt for a password,
parses async, returns a job id, surfaces per-row errors in a review table the user must
resolve before the import commits" is a feature.**

You do this before anyone opens a browser on the app, because the vendor's own docs and the
world's videos will tell you what to look for — including the things behind the login you
may never reach directly.

## Scope — do only this

- **Deliver:** positioning, and a feature inventory specified by behaviour (trigger · inputs ·
  rules · outputs · states) — not by name.
- **Do not:** capture the live product, reconstruct the API, or design the schema. You work
  from what the vendor and the world published; `recon` observes, `api` and `datastore`
  reconstruct. A feature you can only describe from a demo is `EXTERNAL`, never `OBSERVED`.
- **Emit:** the files under `## Emit`, the `intel` slice, and `INT-*` ledger lines. Collect
  `tech_signals` for `datastore` — that is the one thing you gather for another stage.
- **Stop when:** every feature carries its behaviour, not just its name. A list of names is
  not this stage's output and does not close it.

## Load first

- **`bp-mandate`** — read it first, every time. Reading a vendor's public docs, pricing,
  changelog and reviews is ordinary competitive research. Do it without hesitating.
- `bp-manifest`, `bp-evidence` (your prefix is `INT`)
- `blueprint-out/domain/domain-brief.md`, `glossary.md`, `hunt-list.md` — **read these
  properly.** They tell you which features are load-bearing in this domain. A feature that
  implements a hard engine deserves ten times the detail of a settings toggle.
- Web search / fetch. Video access if available.

---

## Method

### 1. The vendor's own words (highest signal-to-noise source that exists)

Read, in this order, and save what you read:

| Source | What to extract |
|---|---|
| Pricing & plans page | Tiers, limits, **entitlements** — feature-gating tells you the module boundaries better than any docs page. What is "Enterprise only" is what is hard or expensive to run. |
| Help centre / knowledge base | The behavioural detail. Support articles describe edge cases, error messages and workarounds — this is where the real spec lives. |
| API / developer docs | Objects, fields, verbs, webhooks, rate limits. If public docs exist, this is a **gift** — it is a partial schema. Save it whole. |
| Feature / tour pages | The claimed capability list. Treat as a checklist to verify, not as truth. |
| Changelog / release notes | Read the last 12–24 months. What they keep fixing = what is fragile. What they recently shipped = where they are going. What they removed = what did not work. |
| Onboarding / getting-started | The intended happy path, step by step. This is the flow your UX must preserve. |
| Status page + incident history | What breaks, how often, which subsystem. Also frequently names infrastructure — hand this to `bp-datastore`. |
| Terms, privacy, trust/security page | Data handling, retention, subprocessors, certifications. **Subprocessor lists name the actual cloud and database vendors.** Hand to `bp-datastore`. |
| Integrations / marketplace | Every third party they connect to. Each is a feature with a contract. |
| Careers / job postings | Engineering roles list the real stack. Hand to `bp-datastore`. |

Save the raw material to `blueprint-out/intel/sources/` so anchors resolve later.

### 2. What the world shows (often the ONLY way to see the logged-in product)

You cannot reach behind the login without credentials. Other people have already filmed it.

- **Video demos & walkthroughs** — vendor demos, YouTube tutorials, webinars, conference
  talks, review-channel deep dives. These show the authenticated UI, real data, real flows.
  For each, save: URL, what it shows, and **`mm:ss` timestamps of the moments that matter**
  (the import flow, the settings panel, the error state, the report output). Write these to
  `blueprint-out/intel/demos.md` so a human can watch the exact seconds.
- **Review sites** — G2, Capterra, TrustRadius, Product Hunt, App/Play store. Read the
  **3-star reviews**, not the 5s and 1s: three-star reviewers describe specific limitations
  precisely. Extract feature confirmations, limits, and complaints (complaints go to Stage 6).
- **Community** — Reddit, HN, Discord/Slack communities, the vendor's own forum. Search
  `site:reddit.com "<product>" problem|limitation|instead|switched`.
- **Third-party tutorials & comparison pages** — often more honest and more detailed than
  the vendor's docs.

Anything only seen in a video is graded `EXTERNAL` and tagged `SEEN-IN-DEMO`. It is strong
evidence and it is **not** `OBSERVED`. Flag these clearly — they are the strongest argument
for asking the user for credentials.

### 3. Build the behavioural inventory

For **every** feature, fill this. If you cannot fill a row, write `unknown — needs recon`
and add it to the hunt list; do not invent it.

```markdown
### F-IMP-03 · Broker contract-note import

- **Purpose** — one sentence, in domain vocabulary (use `glossary.md`)
- **Persona** — who does this, how often
- **Entry points** — every place in the UI (or API, schedule, webhook, email) a user can
  start this flow. Plural: a feature reachable three ways has three entry points.
- **Preconditions** — the state that must already exist before the flow can run (a portfolio
  selected, a file uploaded, a prior step committed).
- **Inputs** — every accepted input: type, format, size limits, required vs optional,
  validation rules. For files: exact formats, per-provider variants.
- **Rules applied** — the business logic, linked to `DOM-*` claims where it implements a
  domain rule. This is the load-bearing row.
- **Outputs** — what the user gets, in what format, with what precision/rounding.
- **Alternate paths** — legitimate variations (a different asset class, a resumed draft, a
  bulk vs single mode). These are real flows, not edge cases.
- **Negative paths** — what the user can do wrong, **what the system must detect, and the
  exact behaviour** it must produce. Not "shows an error" — *which* error, blocking or
  warning, at the field or on the form, and what recovery it offers. In a system where a
  wrong number is worse than a crash, the negative paths *are* the feature; a spec without
  them cannot be tested.
- **States** — every state this feature can be in: empty · loading · partial · success ·
  each distinct error named in the negative paths above.
- **Side effects** — what else changes (notifications, audit entries, downstream recompute)
- **Entitlement** — which plan tier, what limits
- **Evidence** — claim ids
- **Engine?** — does this implement one of the domain's hard engines? Which one?
```

Group features by area, give each a stable `F-<AREA>-<n>` id. These ids are referenced by
every later stage — `bp-ux` specifies screens for them, `bp-gaps` critiques them,
`bp-blueprint` turns them into `FR-*` requirements. **Do not renumber them later.**

### 4. Positioning

Short, sharp, and honest:
- **Category & one-line pitch** (theirs, quoted — and yours, if theirs is fog)
- **ICP** — who actually buys, who actually uses, and whether those are the same people
- **Pricing & packaging** — model (seat/usage/tier/flat), price points, what gates what
- **Claimed differentiators** vs **actual moat** — what they say vs what would genuinely be
  hard to replicate (data, network effects, integrations, regulatory approval, brand trust,
  switching cost). Be blunt: most claimed moats are features.
- **Competitors** and where each wins
- **Where we would position** — one paragraph. Given the domain brief and this product's
  shape, what is the wedge? This feeds Stage 6.

### 5. Reconcile against the domain brief — find the holes on both sides

Cross-check the inventory against `domain-brief.md`. Both directions are findings:

- **Domain rule with no feature** → either they handle it invisibly, or they do not handle
  it. Add to the hunt list. If recon confirms they do not, it is an add-on candidate.
- **Feature with no domain basis** → they invented something. Understand why; it may be
  their real value, or it may be a workaround for a domain problem you missed.
- **Documented feature you cannot find a screen for** → it is behind the login, deprecated,
  or vapour. Add to the hunt list explicitly.

Write this reconciliation as its own section. It is one of the most useful pages in the
whole report.

---

## Proof requirements

- Vendor claims → `DOCUMENTED`, with source URL + **verbatim quote** + retrieval date.
  Paraphrase in your prose if you like; the ledger keeps the exact words.
- Third-party/video → `EXTERNAL`, with URL + quote or `mm:ss` timestamp + what is on screen.
- Your synthesis (positioning, moat assessment, reconciliation) → `INFERRED` with `basis`.
- **A feature row with no evidence field does not go in the inventory.** If you believe a
  feature exists but have nothing to cite, it belongs in the hunt list, not the inventory.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/intel/features.md` | The behavioural inventory (step 3) — the main deliverable |
| `blueprint-out/intel/positioning.md` | Step 4 |
| `blueprint-out/intel/demos.md` | Every video with URL + timestamps + what it shows |
| `blueprint-out/intel/reconciliation.md` | Step 5, both directions |
| `blueprint-out/intel/sources/` | Saved raw material (docs pages, API reference, changelog) |
| `blueprint-out/evidence/ledger.jsonl` | Append `INT-*` claims |

Append to `blueprint-out/domain/hunt-list.md` — the recon targets you discovered (documented
features with no visible screen, flows only seen in demos, entitlements to verify).

Manifest slice `intel`:
```jsonc
"intel": {
  "features": "blueprint-out/intel/features.md",
  "positioning": "blueprint-out/intel/positioning.md",
  "demos": "blueprint-out/intel/demos.md",
  "reconciliation": "blueprint-out/intel/reconciliation.md",
  "feature_ids": ["F-IMP-01","F-IMP-03","F-RPT-01"],
  "feature_count": 47,
  "behind_login_count": 12,
  "tech_signals": [
    {"signal":"Careers page lists 'PostgreSQL, Redis, Kafka'","claim":"INT-031","for":"datastore"}
  ],
  "pricing_tiers": [{"name":"Pro","price":"₹1,999/yr","gates":["F-RPT-04"]}],
  "moat": "..."
}
```
Then `status.intel = "done"`.

Put every infrastructure hint you find — subprocessor lists, job postings, status-page
vendor names, conference talks by their engineers — into `tech_signals`. **Stage 4 depends
on this and cannot easily re-find it.**

---

## Done when

- [ ] Every feature has trigger + inputs + rules + outputs + states filled, or an explicit
      `unknown — needs recon` with a hunt-list entry
- [ ] Every feature that implements a domain hard engine is linked to it
- [ ] Changelog read for ≥12 months, patterns noted
- [ ] Pricing/entitlement map complete — you know what is gated
- [ ] ≥3 demo videos found with timestamps (or an explicit note that none exist)
- [ ] 3-star reviews read, specific limitations extracted
- [ ] Reconciliation done in both directions
- [ ] `tech_signals` populated for `bp-datastore`
- [ ] Ledger self-check passes

---

## Never

- Never ship a feature list of names. If a row could be a bullet on a pricing page, it is
  not finished.
- Never mark something `OBSERVED` — you have not opened the app. That is Stage 2's grade.
- Never take the vendor's differentiator claims at face value. Quote them, then assess them.
- Never skip the help centre because the marketing pages were easier to read. The help
  centre is where the behaviour is.
- Never let a feature you only saw in a video pass as reachable. Tag it `SEEN-IN-DEMO` and
  make the gap visible.
