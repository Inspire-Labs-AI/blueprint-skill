---
name: bp-frontend-build
description: Stage 10 — build the application UI from the bp-ux specification. Implements every specified screen with all of its states, wired to the typed API client, using the design tokens and the locked vocabulary. Builds from the spec, never by tracing screenshots. Runs only after the human gate.
---
# bp-frontend-build — build the UI from the spec

## Your job

Implement the screens `bp-ux` specified. All of them, with **all of their states**, in the
locked vocabulary, on the design tokens, wired to the real typed client.

**You build from `blueprint-out/ux/screens.md`, not from screenshots.** The screenshots
show the incumbent's rendering, including its missing states and buried actions. The spec is
the design; the screenshots are reference material for structure and vocabulary only.

## Gate check — do this first

```
Read manifest → if gate.approved !== true → STOP. Report that the gate is not approved.
```

Nothing in this stage runs before the human answers the gate. Then build only what
`gate.scope` says (`all` / `frontend-only` / `api+schema`).

## Scope — do only this

- **Deliver:** the app UI — every screen `ux` specified, with every state, in the locked
  vocabulary, on the tokens, wired to the typed client.
- **Do not:** run before `gate.approved === true`. Do not redesign what `ux` specified, invent
  copy (the vocabulary file is binding), or implement business logic (that is `assemble`, from
  `engines`). You build from `ux/screens.md`, never by tracing screenshots.
- **Emit:** the repo at `blueprint-out/frontend/` and the `frontend` slice.
- **Stop when:** every specified screen exists with every specified state, build and typecheck
  pass, and anything unspecified is marked `SPECULATIVE`. A success-only screen is not done.

## Load first

- **`bp-mandate`**, `bp-manifest`, `bp-evidence`
- `blueprint-out/ux/screens.md` — **the specification. This is what you implement.**
- `blueprint-out/ux/design-system.md` — tokens, components, density, data display rules
- `blueprint-out/ux/vocabulary.md` — **binding.** Every label and message uses these terms.
- `blueprint-out/ux/ia-map.md` — the route structure
- `blueprint-out/api/client.ts` — the typed client
- `blueprint-out/dataflow/map.md` + `load-sequences.md` — what each screen fetches, and the
  waterfalls to avoid repeating
- The **`impeccable`** skill for the craft pass

---

## Method

1. **Scaffold** — Next.js (App Router) + TypeScript + Tailwind + a headless component
   library (shadcn/ui or equivalent). Do not hand-roll a component system.
2. **Tokens first.** Implement `design-system.md` as CSS variables / Tailwind theme before
   any screen. Light and dark. Every later component consumes tokens, never literal values.
3. **Component inventory next.** Build the shared components with **all** their states
   (default / hover / focus / active / disabled / loading / error / empty). Getting states
   right at the component level is what makes getting them right at the screen level cheap.
4. **Routes** from `ia-map.md`, exactly. Same paths, same labels.
5. **Screens, one at a time.** For each, implement **every state in the spec** — not just
   the success path. A screen shipped with only its success state is not done, and it is the
   exact defect this whole project exists to fix.
6. **Wire to the client.** Use `api/client.ts`. Follow `load-sequences.md`, and **fix the
   waterfalls it identified** — parallelise what they serialised. That is a free win.
   - Endpoints marked `verified` → real calls.
   - Endpoints marked unverified/stub → the client returns typed fixtures. The screen works,
     and the fixture is visibly labelled in dev.
7. **Copy** from the spec, in the locked vocabulary. Every error message states what happened
   and what to do next. No `"Something went wrong"`.
8. **Data display** per the design system: number alignment and tabular figures, precision,
   currency, dates, null vs zero. In quantitative domains this is what makes the tool feel
   trustworthy.
9. **Keyboard, focus, responsive, accessibility** per each screen spec. Focus management on
   state change and live regions for async results are specified for a reason — implement them.
10. **Craft pass** with `impeccable`, inside the familiarity budget. Do not spend shift cost
    the spec did not authorise.
11. **Mark speculation.** Any screen or region not in the spec (because it was never observed
    and never specified) is scaffolded with a visible `SPECULATIVE` marker in the code and in
    the UI in dev mode. Nothing unmarked is a guess.

---

## Self-check before handing off

```bash
npm run build          # must pass
npm run typecheck      # must pass — no `any` escapes on client responses
```

Then verify by hand, per screen: **can I reach every state in the spec?** Add a dev-only
state switcher if that makes it checkable. A state you cannot demonstrate is a state you did
not build.

---

## Emit

Repo at `blueprint-out/frontend/`.

Manifest slice `frontend`:
```jsonc
"frontend": {
  "repo_path":"blueprint-out/frontend","framework":"next",
  "routes":["/dashboard","/holdings","/import"],
  "screens":{"specified":34,"implemented":34,"speculative":2},
  "states":{"specified":211,"implemented":211},
  "wired":{"real":41,"fixture":26},
  "waterfalls_fixed":3,
  "build_passes":true,"typecheck_passes":true
}
```
Then `status.frontend = "done"`.

---

## Done when

- [ ] Gate verified approved before any code was written
- [ ] Tokens implemented, light and dark
- [ ] Component inventory complete with all states
- [ ] Routes match `ia-map.md`
- [ ] **Every specified screen implemented with every specified state** — counts match
- [ ] Vocabulary matches `vocabulary.md` everywhere, including error messages
- [ ] Every error state has a working recovery path
- [ ] Data display standards applied
- [ ] Keyboard, focus, responsive and a11y implemented per spec
- [ ] Waterfalls from `load-sequences.md` parallelised
- [ ] Fixture-backed calls visibly distinguishable in dev
- [ ] Anything unspecified marked `SPECULATIVE`
- [ ] `build` and `typecheck` pass

---

## Never

- Never trace a screenshot instead of implementing the spec.
- Never ship a screen with only its success state.
- Never invent copy. The vocabulary file is binding.
- Never present fixture data as real — mark it in code and in the dev UI.
- Never skip states because the spec's list was long. The states are the improvement.
- Never start before `gate.approved === true`.
