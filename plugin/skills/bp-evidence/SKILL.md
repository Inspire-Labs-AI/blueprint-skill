---
name: bp-evidence
description: The Blueprint proof contract. Defines the five evidence grades, what physically counts as proof for each, and the append-only evidence ledger every claim must be registered in. Load this in EVERY Blueprint stage — a stage that emits claims without ledger entries has not done its job.
---
# bp-evidence — the proof contract

## Your job

Blueprint's entire value is that a reader can **check every sentence**. A claim
without a resolvable pointer to a captured artifact is worthless here — worse than
worthless, because it looks the same as a real finding.

So: **stating something is not enough. Every claim ships with its proof.**

This skill defines what "proof" means, mechanically. Every stage follows it.

---

## The five evidence grades

Every claim you write carries exactly one grade. Pick the *weakest* grade that
honestly applies — never upgrade to sound more confident.

| Grade | Means | Required proof (all fields mandatory) |
|---|---|---|
| `OBSERVED` | You saw it happen in the live product with your own tools | A pointer into a file **on disk in `blueprint-out/`** — HAR entry, screenshot, DOM dump, or JS bundle. See "Anchors" below. |
| `DOCUMENTED` | The vendor says so in their own material | Source URL + a **verbatim quote** (≤300 chars) + retrieval date |
| `EXTERNAL` | A credible third party says so | Source URL + verbatim quote (or video URL + `mm:ss` timestamp + what is on screen) + retrieval date |
| `DOMAIN` | A rule, regulation, standard or spec requires it | Source URL + the **clause/section number** + verbatim quote of the operative text |
| `INFERRED` | You reasoned it out | `basis`: the list of claim IDs this is derived from (must all exist) + `reasoning`: 1–3 sentences + `confidence`: high / medium / low |

**`INFERRED` with an empty `basis` is not a claim. It is a guess. Delete it or go get evidence.**

---

## Anchors — what an `OBSERVED` pointer physically looks like

An anchor must let a human open one file and see the thing. Use the form that matches
the artifact:

| Artifact | Anchor format | Example |
|---|---|---|
| Network capture | `har:<file>#<entry_index>` | `har:recon/traffic.har#412` |
| A specific field in a response | `har:<file>#<entry_index>$.<json_path>` | `har:recon/traffic.har#412$.data.holdings[0].isin` |
| Screenshot | `shot:<file>@<region>` (region = `x,y,w,h` or a described area) | `shot:recon/shots/portfolio.png@main-table` |
| Rendered DOM | `dom:<file>::<css_selector>` | `dom:recon/dom/portfolio.html::table.holdings > tbody > tr:nth-child(1)` |
| JS bundle / source map | `js:<file>#L<line>` | `js:recon/bundles/main.8f2a.js#L14822` |
| Console / storage | `runtime:<file>#<key>` | `runtime:recon/storage/portfolio.json#localStorage.feature_flags` |
| Response header | `hdr:<file>#<entry_index>:<header-name>` | `hdr:recon/traffic.har#412:x-amz-cf-id` |

**Rules for anchors:**
1. The file must exist under `blueprint-out/` at the moment you write the claim. If you
   did not save the artifact, you may not use `OBSERVED`.
2. Paths are relative to `blueprint-out/`. Never absolute, never machine-specific.
3. One anchor is the minimum. For a load-bearing claim (an engine's rule, a schema
   decision, a security finding) give **two or more independent anchors** where possible.
4. If you can only point at something you saw but did not save — **go back and save it
   first.** Re-capture is cheap; an unverifiable report is not.

---

## The ledger — `blueprint-out/evidence/ledger.jsonl`

Append-only. One JSON object per line. Every stage appends its claims. Never rewrite or
delete another stage's lines.

```jsonc
{"id":"API-014","stage":"api","grade":"OBSERVED","claim":"POST /v2/holdings/import accepts a multipart CSV and returns a job id, not the parsed result — the import is asynchronous.","anchors":["har:recon/traffic.har#0412","har:recon/traffic.har#0418$.job_id"],"tags":["api","async","import"]}
{"id":"DS-007","stage":"datastore","grade":"INFERRED","claim":"Primary transactional store is PostgreSQL.","basis":["DS-003","DS-004","DS-006"],"reasoning":"IDs are sequential 64-bit integers with no gaps across a 40-row page; list endpoints use offset+limit rather than opaque cursors; the trust page names Amazon RDS as a subprocessor.","confidence":"high","tags":["datastore","tech"]}
{"id":"DOM-021","stage":"domain","grade":"DOMAIN","claim":"Long-term gains on listed equity are grandfathered to the higher of actual cost and 31-Jan-2018 FMV.","source":"https://incometaxindia.gov.in/...","clause":"s.112A(5) proviso","quote":"...the cost of acquisition shall be deemed to be the higher of...","retrieved":"2026-08-26","tags":["domain","tax","engine:gains"]}
```

**Required fields by grade**

- always: `id`, `stage`, `grade`, `claim`, `tags`
- `OBSERVED`: `anchors` (≥1)
- `DOCUMENTED` / `EXTERNAL`: `source`, `quote` (or `timestamp` for video), `retrieved`
- `DOMAIN`: `source`, `clause`, `quote`, `retrieved`
- `INFERRED`: `basis` (≥1 existing claim id), `reasoning`, `confidence`

**ID format:** `<STAGE-PREFIX>-<3 digits>`, zero-padded, unique forever.
`DOM` domain · `INT` intel · `REC` recon · `API` api · `DS` datastore · `ENG` engines ·
`GAP` gaps · `FLW` dataflow · `UX` ux · `SEC` security finding.

---

## How to use it while working

1. **Capture first, claim second.** If you are about to write a sentence and you cannot
   name the file it came from, you are guessing. Go capture it.
2. **Write the ledger line at the moment you learn the thing**, not at the end. Batching
   at the end is how anchors get invented.
3. **In prose, cite the id.** Write claims in your documents as
   `... the import is asynchronous [API-014].` The id resolves to the ledger, the ledger
   resolves to the file. That is the chain.
4. **When you infer, list the ids you inferred from.** `basis: ["DS-003","DS-004"]` is
   what turns a guess into an argument.
5. **Contradictions are findings, not errors.** If two sources disagree, log both and add
   a third `INFERRED` claim that adjudicates, with reasoning.

---

## Verify before you hand off (mechanical self-check)

Run this at the end of your stage. Fix everything it flags. Do not report `done` with
failures outstanding.

```bash
# 1. Every OBSERVED anchor resolves to a file that exists
grep '"grade":"OBSERVED"' blueprint-out/evidence/ledger.jsonl \
  | grep -o '"anchors":\[[^]]*\]' | grep -o '[a-z]*:[^"#@:]*' | cut -d: -f2 | sort -u \
  | while read -r f; do [ -e "blueprint-out/$f" ] || echo "MISSING ARTIFACT: $f"; done

# 2. Every INFERRED basis id exists in the ledger
# 3. No duplicate ids
cut -d'"' -f4 blueprint-out/evidence/ledger.jsonl | sort | uniq -d
```

Then answer these in your handoff notes:

- How many claims did I log? How many are `OBSERVED` vs `INFERRED`?
- Which of my load-bearing claims rests on a **single** anchor? (Those are the fragile ones — say so.)
- What did I want to prove and could not? (Name it. An honest gap beats a soft claim.)

---

## Never

- Never write `OBSERVED` for something you reasoned, remembered, or read in docs.
- Never invent an anchor, a line number, a quote, or a clause reference. If you are not
  certain of the exact citation, use a weaker grade and say the citation is approximate.
- Never present a behind-login screen, an unreached endpoint, or a guessed schema as real.
- Never delete or edit another stage's ledger lines. Append a correcting claim instead,
  with `"supersedes":"<id>"`.
- Never let "confidence: high" stand in for evidence. Confidence is your opinion; anchors
  are the proof.
