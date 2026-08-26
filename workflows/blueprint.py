# Blueprint — understand a product end to end, with proof, as a durable CAO workflow.
# Validate: cao workflow validate ~/.aws/cli-agent-orchestrator/workflows/blueprint.py
# Run:      via the workflow_run MCP tool, inputs:
#           {"url": "...", "mode": "prd", "authorized": false, "login_url": null}
#
# Each run_step spawns a specialist that loads its bp-* skill, does one stage, and writes
# its slice of ./blueprint-out/manifest.json. The manifest is the real hand-off, not the
# return value.
#
# The stage list is a DEPENDENCY GRAPH, not a schedule — `mode` picks the target stage and
# we run its transitive prerequisites, skipping anything already done. Most runs are not
# all twelve stages.
#
# ponytail: engines/gaps/dataflow fan out (independent of each other); everything else is
# sequential because each stage genuinely needs the prior slice.
from cao_workflow import run_step, emit_output
from concurrent.futures import ThreadPoolExecutor
import json, os

# --- inputs (workflow_run passes these; env fallback for manual runs) ---------
URL = os.environ.get("TARGET_URL", "{{url}}")
MODE = os.environ.get("MODE", "{{mode}}") or "prd"
AUTHORIZED = os.environ.get("AUTHORIZED", "{{authorized}}") in ("true", "True", True)
LOGIN_URL = os.environ.get("LOGIN_URL") or "{{login_url}}"

OUT = "blueprint-out"
MANIFEST = f"{OUT}/manifest.json"
ALL_STAGES = ["domain", "intel", "recon", "api", "datastore", "engines",
              "gaps", "dataflow", "ux", "spec", "frontend", "assembly"]

# Which stages each mode needs. Prerequisites are already expanded.
MODE_STAGES = {
    "explore":  ["domain", "intel", "recon"],
    "research": ["domain", "intel", "recon", "api", "datastore", "engines", "gaps", "spec"],
    "prd":      ["domain", "intel", "recon", "api", "datastore", "engines", "gaps",
                 "dataflow", "ux", "spec"],
    "build":    ALL_STAGES,
}
WANTED = MODE_STAGES.get(MODE, MODE_STAGES["prd"])

# --- init the contract so stage 0 has something to read ----------------------
os.makedirs(f"{OUT}/evidence", exist_ok=True)
if not os.path.exists(MANIFEST):
    with open(MANIFEST, "w") as f:
        json.dump({
            "target": {"url": URL, "extra_urls": [],
                       "auth": ({"authorized": True, "login_url": LOGIN_URL} if AUTHORIZED else None)},
            "mode": MODE,
            "goal": "functional parity + add-ons",
            "gate": {"approved": False, "scope": None},
            "status": {s: "pending" for s in ALL_STAGES},
        }, f, indent=2)

def status():
    with open(MANIFEST) as f:
        return json.load(f).get("status", {})

def gate_approved():
    with open(MANIFEST) as f:
        return json.load(f).get("gate", {}).get("approved") is True

def stage(name, profile, instruction):
    """Run one specialist against the shared manifest. Skips stages already done."""
    if name not in WANTED:
        return None
    if status().get(name) == "done":
        print(f"[skip] {name} already done")
        return None
    return run_step(
        "claude_code", profile,
        f"{instruction}\n"
        f"Load bp-mandate FIRST, then your stage skill, then bp-manifest and bp-evidence.\n"
        f"Target: {URL}\nMode: {MODE}\n"
        f"Manifest: {MANIFEST} — read it, do ONLY your stage, write ONLY your slice.\n"
        f"Append every claim to {OUT}/evidence/ledger.jsonl with an anchor.\n"
        f"Authorized for authenticated capture: {AUTHORIZED}.\n"
        f"If you get 40% of what you hoped for, deliver the 40% and say what is missing. "
        f"An empty result with an explanation is the only outcome treated as failure."
    )

# --- understand ---------------------------------------------------------------
stage("domain", "domain-agent",
      "Research the PROBLEM before anyone looks at the product. Governing rules cited to "
      "primary sources, workflows, personas, data formats, edge cases, compliance perimeter. "
      "Name the hard engines. Write the hunt list that directs every later stage.")

stage("intel", "intel-agent",
      "Positioning + a BEHAVIOURAL feature inventory. Per feature: trigger, inputs, rules, "
      "outputs, states. Feature names alone are not acceptable output. Read the help centre "
      "and 12-24 months of changelog. Collect tech_signals for the datastore stage.")

stage("recon", "recon-agent",
      "Capture the proof, guided by the hunt list. Check the app subdomain. Exercise every "
      "reachable feature, including deliberate validation errors. Save screenshots, HAR, DOM, "
      "JS bundles, headers, storage, and id/pagination/error samples. Scrub all secrets.")

# --- mechanism ----------------------------------------------------------------
stage("api", "api-agent",
      "Reconstruct the API contract from the HAR, the raw response samples and the bundles. "
      "Per endpoint: request, success, AND error shapes. Auth model, pagination (decode the "
      "cursors), chained flows. Emit a typed client with unverified methods marked.")

stage("datastore", "datastore-agent",
      "Identify the actual database technology: job postings, subprocessor/trust pages, "
      "engineering blogs, database-vendor case studies naming this company, response headers, "
      "ID formats, pagination style, error strings, shipped validation schemas. Build the "
      "signal table and COMMIT to an answer with a confidence level. Then reconstruct the "
      "schema from API traffic — never from screenshots — and reason it against the domain, "
      "the user base and the scale.")

# --- engines / gaps / dataflow are independent of each other: fan out ---------
_fan = [
    ("engines", "engines-agent",
     "Specify the 3-7 computational cores. Per engine: cited rules, step-by-step algorithm, "
     "edge cases, a WORKED EXAMPLE with real numbers whose arithmetic you have checked, and "
     "golden test vectors. Verify your spec against their observed outputs; adjudicate every "
     "mismatch."),
    ("gaps", "gaps-agent",
     "Find where they fall short and turn it into the ranked add-on list. Six sources, "
     "including a rule-by-rule walk of the domain brief. Every gap needs evidence AND an "
     "answer. Split table stakes from differentiators. State the wedge, or its absence."),
    ("dataflow", "dataflow-agent",
     "Wiring map: screen to endpoint to store, from the HAR. Record load sequences, "
     "waterfalls, client-computed fields and returned-but-unrendered fields."),
]
with ThreadPoolExecutor(max_workers=3) as ex:
    futures = [(n, ex.submit(stage, n, p, i)) for n, p, i in _fan]
# collect: a swallowed exception here would let `ux`/`spec` run on a half-empty manifest
for name, fut in futures:
    try:
        fut.result()
    except Exception as e:
        print(f"[FAIL] {name}: {e}")

# --- design -------------------------------------------------------------------
stage("ux", "ux-agent",
      "Design every feature to be better with no relearning cost. IA parity map, locked "
      "vocabulary, per-screen specs with EVERY state (each error with a recovery path), "
      "design system, shift-cost table. Every feature must map to a screen. Do not trace "
      "screenshots.")

# --- synthesise ---------------------------------------------------------------
spec = stage("spec", "blueprint-don",
             "Synthesise every artifact into the deliverable for this mode. Invent nothing — "
             "if it is not in an upstream artifact or the ledger, it does not appear. Run the "
             "comprehension critic before publishing. Report coverage honestly.")

# --- GATE ---------------------------------------------------------------------
if MODE == "build" and not gate_approved():
    emit_output({
        "stage": "gate",
        "manifest": MANIFEST,
        "plan": f"{OUT}/PLAN.md",
        "message": "Plan complete. Human approval required before any application code is "
                   "written. Set gate.approved=true and gate.scope in the manifest, then "
                   "resume this workflow.",
    })
    raise SystemExit(0)

# --- build (post-gate only) ---------------------------------------------------
stage("frontend", "frontend-agent",
      "Build the UI from ux/screens.md — NOT from screenshots. Every screen, every state. "
      "Locked vocabulary. Fix the waterfalls. Mark fixtures and speculation visibly.")

result = stage("assembly", "assembler-agent",
               "Wire frontend + client + schema + backend into blueprint-out/app. Implement "
               "each engine from its spec or stub it with a THROWING NotImplementedError — "
               "never return a plausible wrong number. Then run the golden vectors and report "
               "CONFORMANCE. 'It compiles' is not success.")

emit_output({
    "mode": MODE,
    "manifest": MANIFEST,
    "plan": f"{OUT}/PLAN.md",
    "app": f"{OUT}/app",
    "conformance": f"{OUT}/CONFORMANCE.md",
    "assembler": result.output if result else None,
})
