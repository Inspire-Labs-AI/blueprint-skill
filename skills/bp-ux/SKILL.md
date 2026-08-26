---
name: bp-ux
description: Stage 8 — design every feature to be better without making users relearn anything. Enforces a familiarity budget - keep the vocabulary, information architecture and flow order users are habituated to; improve the mechanics, feedback, states, speed and error recovery. Produces the IA parity map, per-screen shift-cost table, design tokens, component inventory and full state matrix that the build works from. Screens are specified from behaviour, never traced from screenshots.
---
# bp-ux — familiar to use, better to use

## Your job

Design the product so that a user of the incumbent can sit down and be productive
**immediately**, and then find that everything works better than they expected.

Two forces pull against each other and both are real:

- **Habituation is an asset.** A professional who runs this workflow every day has the
  layout in muscle memory. Every change you make spends some of their goodwill. Change the
  words for their domain concepts and they are lost. Move the primary action and they hunt
  for it. Re-sequence the flow they run fifty times a week and you have made their day
  worse, no matter how much more logical your order is.
- **Copying their interface copies their mistakes.** Their dated patterns, missing states,
  buried actions and unhelpful errors are not sacred. Reproducing them is not respect for
  the user, it is laziness.

The resolution: **keep the map, upgrade the road.**

Preserve what users navigate by — vocabulary, structure, flow order, where things live.
Improve everything about how it actually works — speed, feedback, states, error recovery,
defaults, bulk operations, accessibility.

**Do not trace screenshots.** You are designing screens that deliver the *behaviour* from
`bp-intel` and the *add-ons* from `bp-gaps`, at a quality bar theirs does not meet.

## Load first

- **`bp-mandate`** — read it first. Deliver a complete design spec; do not hedge it into
  suggestions.
- `bp-manifest`, `bp-evidence` (your prefix is `UX`)
- `blueprint-out/intel/features.md` — **every feature must be delivered.** Parity is
  functional, and this stage is where "all features" is enforced.
- `blueprint-out/domain/glossary.md` — **the vocabulary is not yours to change.**
- `blueprint-out/recon/shots/` + `dom/` — reference for structure and vocabulary, **not** a
  visual target
- `blueprint-out/recon/coverage.md` — which states were actually captured
- `blueprint-out/gaps/addons.md` — the UX gaps are your brief
- `blueprint-out/api/` + `blueprint-out/dataflow/` — what each screen can actually load
- The **`impeccable`** skill for the visual and interaction craft pass

---

## The familiarity budget

Every difference from the incumbent has a **shift cost** — how much relearning it forces.
You are spending a limited budget. Spend it only where the payoff is large.

| Shift cost | What it means | Rule |
|---|---|---|
| **none** | Users will not notice a change. Faster loads, better errors, added states, keyboard shortcuts, an empty state where there was none. | Do these freely. Most of your improvements live here. |
| **low** | Noticeable, instantly understood. Restyled component, denser table, an added bulk action, an inline hint. | Do these freely. |
| **medium** | Requires a moment of orientation. A moved secondary action, a merged pair of screens, a changed default. | Needs a stated justification tied to a `GAP-*`. |
| **high** | Forces relearning. Renamed domain concept, restructured navigation, re-sequenced core flow, removed a familiar affordance. | **Needs a strong justification, and an in-product affordance that helps users bridge it.** Aim for zero to three of these in the entire product. |

### The four rules that are close to absolute

1. **Never rename a domain concept the user knows.** If the industry and the incumbent both
   say "contract note", you say "contract note". Not "trade document", not "statement". The
   glossary from `bp-domain` is binding. Renaming domain vocabulary is the fastest way to
   make an expert feel lost and a product feel amateur.
2. **Never move the primary action of a screen** to a different region. If their save is
   bottom-right, yours is bottom-right.
3. **Never re-sequence a flow the user runs frequently.** You may make steps faster, merge a
   step that was pure friction, or let people skip ahead — but the mental model of the
   sequence stays.
4. **Never remove an affordance without replacing it.** If a power user relies on a filter,
   an export, or a keyboard path, it exists in ours. Removing capability in the name of
   simplicity is how rebuilds lose the exact users who care most.

Everything not covered by those four is fair game for improvement.

---

## Method

### 1. IA parity map

Map their structure to ours, route by route:

```markdown
| Their route | Their label | Our route | Our label | Shift | Why |
|---|---|---|---|---|---|
| /dashboard | Dashboard | /dashboard | Dashboard | none | — |
| /holdings | My Holdings | /holdings | My Holdings | none | — |
| /reports/cg | Capital Gains | /reports/capital-gains | Capital Gains | none | cleaner URL, same label and position |
| /import + /import/history | Import / History | /import | Import | medium | merged; history is a tab. GAP-11: users lost track of past imports. Tab preserves both entry points. |
```

Default to matching. **Every difference needs a reason in that last column.** If the reason
column says "cleaner" with no gap reference, revert it — that is budget spent on your taste.

Also preserve URL shapes where reasonable. People bookmark and share links.

### 2. Vocabulary lock

Produce the term list: their term · industry term · our term · same? If any row differs,
justify it against the glossary. Expect this list to be almost entirely "same".

This list is binding on every later stage — copy, labels, error messages, the API client,
the schema. **One product, one vocabulary.**

### 3. Screen specifications — from behaviour, with every state

For every feature in `features.md`, specify its screen(s):

```markdown
### S-IMP-01 · Import

- **Delivers** — F-IMP-03, F-IMP-04 · **Add-ons** — GAP-07, GAP-11
- **Purpose** — one sentence in domain vocabulary
- **Persona & frequency** — who, how often, under what time pressure
- **Entry points** — how users arrive
- **Layout** — regions and hierarchy. What is primary, secondary, tertiary. Where the
  primary action sits (**match theirs**).
- **Data** — which endpoints load it, what is above the fold, what is deferred
- **States** — every one, specified, not listed:
  - **empty** (first ever use — this is an onboarding surface, not a blank page)
  - **empty** (filtered to nothing — different message, offer to clear the filter)
  - **loading** (skeleton matching final layout; never a spinner over a blank region)
  - **partial** (some data, some still loading)
  - **success**
  - **error**, one per real failure mode from the API's error taxonomy, **each with a
    recovery path** — what the user does next, in the UI, without contacting support
  - **permission denied** · **stale/offline** if applicable
- **Interactions** — per action: trigger, feedback, optimistic or not, undo?, confirm?
- **Keyboard** — shortcuts, tab order, focus management on state change
- **Responsive** — what changes at each breakpoint; what a table becomes on mobile
- **Accessibility** — landmarks, live regions for async results, labels, contrast, focus traps
- **Copy** — real strings, in domain vocabulary. Every error message says what happened and
  what to do next.
- **Acceptance** — Given/When/Then for the load-bearing behaviour
- **Shift from theirs** — none/low/medium/high + justification
- **Mockup** — a rendered `.mock` HTML block for `PRD.html` (see the template's `.screen > .mock`)
```

**The states section is where most of the improvement lives, and it is the section people
skip.** Incumbents typically ship the success state and half an error state. Specifying all
of them is most of what "better UX, no relearning" actually means in practice.

### 4. Design system

- **Tokens** — colour (semantic, not literal: `surface`, `text-muted`, `danger`), type scale,
  spacing scale, radii, shadows, motion durations and easings. Light and dark.
- **Component inventory** — every component the screens need, with all its variants and
  states (default/hover/focus/active/disabled/loading/error). Build from an existing
  headless library; do not hand-roll a design system for one product.
- **Density** — professional tools need dense layouts. If the domain persona reviews
  thousands of rows, default to compact and offer comfortable, not the reverse.
- **Data display standards** — number and date formatting, alignment (**numbers right-aligned,
  tabular figures**), currency, precision, negative-value treatment, null vs zero. In a
  financial or quantitative domain, get this right; it is what makes a tool feel trustworthy.
- **Motion** — purposeful only: state transitions, spatial continuity. Nothing decorative on
  a screen someone uses fifty times a day.

Run the visual craft pass through the **`impeccable`** skill. Raise the bar past the
reference — but inside the familiarity budget.

### 5. Flow specifications

For each core workflow: the step sequence (**matching theirs unless justified**), what
carries between steps, where it can be saved and resumed, where it can fail and how the user
recovers, and the friction you removed with the `GAP-*` that justifies each removal.

Count the interactions for their version and ours. `12 clicks → 4 clicks` is the kind of
concrete claim the PRD should carry.

### 6. The shift-cost summary

One table, every difference in the product, sorted by cost. This is the page a stakeholder
reads to understand what changes for existing users. Totals at the bottom.

If you have more than three `high` rows, cut some. You are overspending the budget.

---

## Proof requirements

- Every "theirs does X" statement anchors to a screenshot, DOM node, or HAR entry.
- Every improvement links to a `GAP-*` or is a `none`-cost improvement (states, speed,
  a11y, keyboard) that needs no separate justification.
- Every `medium`/`high` shift has an explicit written justification.
- Every feature in `features.md` maps to at least one screen. **Unmapped features are a
  parity failure** — list them explicitly with the reason.
- States you never observed are marked `INFERRED` — you are designing them from the API's
  error taxonomy, which is legitimate and must be labelled.

---

## Emit

| File | Contents |
|---|---|
| `blueprint-out/ux/ia-map.md` | Route-by-route parity map |
| `blueprint-out/ux/vocabulary.md` | The binding term list |
| `blueprint-out/ux/screens.md` | All screen specifications |
| `blueprint-out/ux/design-system.md` | Tokens, components, density, data display, motion |
| `blueprint-out/ux/flows.md` | Core workflows, before/after interaction counts |
| `blueprint-out/ux/shift-cost.md` | The summary table |
| `blueprint-out/ux/mocks/` | Rendered `.mock` HTML per screen for `PRD.html` |
| `blueprint-out/evidence/ledger.jsonl` | Append `UX-*` |

Manifest slice `ux`:
```jsonc
"ux": {
  "ia_map":"blueprint-out/ux/ia-map.md","screens":"blueprint-out/ux/screens.md",
  "design_system":"blueprint-out/ux/design-system.md","vocabulary":"blueprint-out/ux/vocabulary.md",
  "screens_specified":34,
  "feature_coverage":{"total":47,"mapped":47,"unmapped":[]},
  "shift_cost":{"none":58,"low":19,"medium":6,"high":2},
  "high_shifts":[{"what":"merged import + history","why":"GAP-11","bridge":"tab preserves both entry points"}],
  "states_specified":211,
  "flow_improvements":[{"flow":"import","their_clicks":12,"our_clicks":4,"gap":"GAP-07"}]
}
```
Then `status.ux = "done"`.

---

## Done when

- [ ] **Every feature in `features.md` maps to a screen** — `unmapped` is empty, or each
      entry has a stated reason
- [ ] IA parity map complete; every difference justified in its own column
- [ ] Vocabulary locked against the domain glossary
- [ ] Every screen has **every** state specified, each error with a recovery path
- [ ] Design tokens and component inventory complete, light and dark
- [ ] Data display standards set (alignment, precision, currency, null vs zero)
- [ ] Keyboard, responsive and accessibility specified per screen
- [ ] Core flows specified with before/after interaction counts
- [ ] Shift-cost table complete; ≤3 `high` rows, each with a bridge affordance
- [ ] Mockups rendered for `PRD.html`
- [ ] Ledger self-check passes

---

## Never

- Never trace a screenshot. Specify from behaviour.
- Never rename a domain concept. The glossary is binding.
- Never move the primary action or re-sequence a frequent flow without a `GAP-*` and a bridge.
- Never drop a feature because it seemed minor. Parity is functional and it is the floor.
- Never ship a screen spec with only the success state. That is the incumbent's mistake and
  it is the one you are here to fix.
- Never spend familiarity budget on personal taste. If the justification column cannot cite
  a gap, revert the change.
- Never let "modernise the design" become "make experts relearn their job".
