# Blueprint — end-to-end product clone as a durable CAO workflow.
# Validate: cao workflow validate ~/.aws/cli-agent-orchestrator/workflows/blueprint.py
# Run:      via the workflow_run MCP tool, inputs: {"url": "...", "authorized": false, "login_url": null}
#
# Each run_step spawns a specialist CAO agent that loads its bp-* skill, does one
# stage, and writes its slice of ./blueprint-out/manifest.json. We pass the manifest
# path + target in every prompt; the manifest is the real hand-off, not the return.
#
# ponytail: db + api fan out concurrently (both only depend on recon+intel).
# Everything else is sequential because each stage genuinely needs the prior slice.
from cao_workflow import run_step, emit_output
from concurrent.futures import ThreadPoolExecutor
import json, os

# --- inputs (workflow_run passes these; fall back to env for manual runs) ---
URL = os.environ.get("TARGET_URL", "{{url}}")
AUTHORIZED = os.environ.get("AUTHORIZED", "{{authorized}}") in ("true", "True", True)
LOGIN_URL = os.environ.get("LOGIN_URL") or "{{login_url}}"

OUT = "blueprint-out"
MANIFEST = f"{OUT}/manifest.json"

# --- init the contract so stage 0 has something to read ---
os.makedirs(OUT, exist_ok=True)
if not os.path.exists(MANIFEST):
    with open(MANIFEST, "w") as f:
        json.dump({
            "target": {"url": URL, "auth": ({"authorized": True, "login_url": LOGIN_URL} if AUTHORIZED else None)},
            "status": {k: "pending" for k in ["recon", "intel", "database", "api", "dataflow", "frontend", "assembly"]},
        }, f, indent=2)

def stage(profile, instruction):
    """Run one specialist against the shared manifest."""
    return run_step("claude_code", profile,
        f"{instruction}\nTarget: {URL}\nManifest: {MANIFEST} (read it, do your stage, write your slice). "
        f"Authorized for live capture/replication: {AUTHORIZED}.")

# Stage 0 — recon (everything downstream needs the captures first)
stage("recon-agent", "Capture the target: screenshots, HAR (only if authorized), DOM, routes.")

# Stage 1 — intel
stage("intel-agent", "Reverse-engineer the SaaS into feature map, tech stack, moat, priorities.")

# Stages 2 + 3 — DB and API are independent; fan out.
with ThreadPoolExecutor(max_workers=2) as ex:
    ex.submit(stage, "db-agent",  "Infer DB schema from the screenshots (screenshot2sql).")
    ex.submit(stage, "api-agent", "Map the backend API: live from HAR if authorized, else infer from screenshots.")

# Stage 4 — dataflow fusion (needs recon+intel+db+api all done)
stage("dataflow-agent", "Fuse everything into the UI->API->DB end-to-end map + Mermaid diagram.")

# Stage 5 — frontend (reads dataflow.map so sections know their data)
stage("frontend-agent", "Clone the UI into a Next.js repo via /clone-website, wired to dataflow.map.")

# Stage 6 — assemble into one runnable repo
result = stage("assembler-agent", "Wire frontend + API client + schema into blueprint-out/app and verify it builds.")

emit_output({"manifest": MANIFEST, "app": f"{OUT}/app", "assembler": result.output})
