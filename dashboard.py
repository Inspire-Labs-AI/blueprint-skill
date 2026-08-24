#!/usr/bin/env python3
# Simple Blueprint dashboard. Loops: read CAO sessions + manifest -> write a
# self-refreshing board.html on the mounted volume. Open it in your Windows browser:
#   C:\Users\JyothiKumar\Desktop\work\blueprint\run\blueprint-out\board.html
# Run inside the container:  python3 dashboard.py   (Ctrl-C to stop)
# ponytail: bakes data into the file + <meta refresh>. No server, no ports, no CORS.
import json, time, os, urllib.request

OUT = "run/blueprint-out"
BOARD = f"{OUT}/board.html"
STAGES = ["recon", "intel", "database", "api", "dataflow", "frontend", "assembly"]
COLOR = {"done": "#22c55e", "running": "#3b82f6", "failed": "#ef4444",
         "pending": "#6b7280", "inferred-only (no HAR)": "#eab308"}

def cao_sessions():
    try:
        with urllib.request.urlopen("http://127.0.0.1:9889/sessions", timeout=3) as r:
            return json.load(r)
    except Exception as e:
        return {"error": str(e)}

def read_manifest():
    try:
        with open(f"{OUT}/manifest.json") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def pill(label, state):
    c = COLOR.get(str(state), "#eab308")
    return f'<span class="pill" style="background:{c}">{label}: {state}</span>'

def render(m, sess):
    # stage status: support both the pipeline schema (status{}) and synthesis schema (slices{})
    status = m.get("status") or m.get("slices") or {}
    keys = STAGES if m.get("status") else list(status.keys())
    stage_html = "".join(pill(k, status.get(k, "pending")) for k in keys) or "<i>no stages yet</i>"
    sess_rows = ""
    if isinstance(sess, list):
        for s in sess:
            sess_rows += f"<tr><td>{s.get('id','?')}</td><td>{s.get('status','?')}</td><td>{s.get('terminals','?')}</td></tr>"
    elif isinstance(sess, dict) and sess.get("error"):
        sess_rows = f'<tr><td colspan=3><i>server: {sess["error"]}</i></td></tr>'
    target = m.get("target", "—")
    if isinstance(target, dict): target = target.get("url", "—")
    SKIP = {"node_modules", ".next", ".git", ".cache", "dist", "build"}
    files = []
    for root, dirs, fs in os.walk(OUT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in fs:
            if f == "board.html":
                continue
            files.append(os.path.join(root, f).replace(OUT + "/", ""))
    files = sorted(files)
    shown, extra = files[:80], max(0, len(files) - 80)
    files_html = "".join(f"<li>{f}</li>" for f in shown) or "<li><i>none yet</i></li>"
    if extra:
        files_html += f"<li><i>… +{extra} more (node_modules hidden)</i></li>"
    return f"""<!doctype html><html><head><meta charset=utf-8>
<meta http-equiv=refresh content=3>
<title>Blueprint — {target}</title>
<style>
 body{{font:14px system-ui;background:#0b0f17;color:#e5e7eb;margin:0;padding:24px}}
 h1{{font-size:18px;margin:0 0 4px}} .sub{{color:#9ca3af;margin-bottom:20px}}
 .card{{background:#111827;border:1px solid #1f2937;border-radius:10px;padding:16px;margin-bottom:16px}}
 .pill{{display:inline-block;color:#0b0f17;font-weight:600;padding:4px 10px;border-radius:999px;margin:4px}}
 table{{width:100%;border-collapse:collapse}} td,th{{text-align:left;padding:6px 8px;border-bottom:1px solid #1f2937}}
 code{{color:#93c5fd}} ul{{columns:2;margin:0;padding-left:18px}}
</style></head><body>
<h1>🧬 Blueprint pipeline</h1>
<div class=sub>target <code>{target}</code> · auto-refresh 3s · {time.strftime('%H:%M:%S')}</div>
<div class=card><b>Stages</b><br>{stage_html}</div>
<div class=card><b>CAO sessions</b><table><tr><th>id</th><th>status</th><th>terminals</th></tr>{sess_rows}</table></div>
<div class=card><b>Artifacts in {OUT}/</b><ul>{files_html}</ul></div>
</body></html>"""

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"writing {BOARD} every 3s — open it in your browser. Ctrl-C to stop.")
    while True:
        html = render(read_manifest(), cao_sessions())
        with open(BOARD, "w", encoding="utf-8") as f:
            f.write(html)
        time.sleep(3)
