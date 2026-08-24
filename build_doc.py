#!/usr/bin/env python3
# Generates a self-contained executive HTML brief (images embedded as base64, no paths).
import base64, os

SHOTS = "run/blueprint-out/recon/shots"
PICKS = [("pricing.png","Captured: Pricing page"),
         ("buy.png","Captured: Buy / checkout entry"),
         ("login.png","Captured: Auth wall — product API lives beyond this"),
         ("sign_up.png","Captured: Sign-up funnel")]

def img(name):
    p = os.path.join(SHOTS, name)
    if not os.path.exists(p): return None
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

cards = ""
for name, cap in PICKS:
    d = img(name)
    if d:
        cards += f'<figure><img src="{d}" alt="{cap}"/><figcaption>{cap}</figcaption></figure>\n'

HTML = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>Blueprint — Web-App Cloning Initiative</title>
<style>
 :root{{--bg:#0b1020;--card:#141a2e;--ink:#e8ecf6;--mut:#9aa4c0;--line:#26304d;
   --acc:#6ea8fe;--good:#38d39f;--warn:#f6c453;--bad:#ff6b6b;}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);
   font:16px/1.6 -apple-system,Segoe UI,Roboto,Inter,sans-serif}}
 .wrap{{max-width:920px;margin:0 auto;padding:48px 24px}}
 header{{border-bottom:1px solid var(--line);padding-bottom:24px;margin-bottom:32px}}
 .kicker{{color:var(--acc);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:12px}}
 h1{{font-size:34px;margin:8px 0 6px;line-height:1.15}}
 .sub{{color:var(--mut);font-size:15px}}
 h2{{font-size:21px;margin:38px 0 12px;display:flex;align-items:center;gap:10px}}
 h2::before{{content:"";width:6px;height:22px;background:var(--acc);border-radius:3px}}
 p{{color:#d7ddf0}} .mut{{color:var(--mut)}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:14px 0}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
 @media(max-width:640px){{.grid{{grid-template-columns:1fr}}}}
 .tag{{display:inline-block;font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px}}
 .t-bad{{background:rgba(255,107,107,.15);color:var(--bad)}}
 .t-good{{background:rgba(56,211,159,.15);color:var(--good)}}
 .t-warn{{background:rgba(246,196,83,.15);color:var(--warn)}}
 table{{width:100%;border-collapse:collapse;font-size:14.5px}}
 th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
 th{{color:var(--mut);font-weight:600}}
 ul{{margin:8px 0;padding-left:20px}} li{{margin:4px 0}}
 .gallery{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px}}
 @media(max-width:640px){{.gallery{{grid-template-columns:1fr}}}}
 figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
 figure img{{width:100%;display:block;max-height:230px;object-fit:cover;object-position:top}}
 figcaption{{padding:9px 12px;font-size:12.5px;color:var(--mut)}}
 .steps{{counter-reset:s;list-style:none;padding:0}}
 .steps li{{counter-increment:s;position:relative;padding:10px 0 10px 42px;border-bottom:1px solid var(--line)}}
 .steps li::before{{content:counter(s);position:absolute;left:0;top:8px;width:28px;height:28px;
   background:var(--acc);color:#0b1020;font-weight:800;border-radius:50%;display:grid;place-items:center;font-size:14px}}
 .big{{font-size:15px}} b{{color:#fff}}
 footer{{margin-top:40px;border-top:1px solid var(--line);padding-top:18px;color:var(--mut);font-size:13px}}
</style></head><body><div class=wrap>

<header>
 <div class=kicker>Cloning Initiative · Executive Brief</div>
 <h1>Blueprint: an autonomous agent to reverse-engineer &amp; clone web apps</h1>
 <div class=sub>The problem with naive cloning, and the evidence-first approach we built to fix it.</div>
</header>

<h2>The issue</h2>
<div class=card>
 <p>Our first cloning attempts <b>looked</b> complete but were <b>fabricated</b>. An agent
 pointed at a product would screenshot the public pages and then <span class="tag t-bad">hallucinate</span>
 a backend, database schema, and even "logged-in" screens it had never actually seen.</p>
 <div class=grid style="margin-top:6px">
  <div><b>Symptom</b><ul class=mut>
    <li>Post-login UI generated from guesswork, presented as real</li>
    <li>APIs & DB schema invented from screenshots</li>
    <li>No real network/API inspection — the actual product surface was never captured</li>
    <li>Bad aesthetics, no system design, no credible estimate</li></ul></div>
  <div><b>Root cause</b><ul class=mut>
    <li>Modern apps are <b>API-driven</b> — the product lives in network traffic and JS
    bundles, not the rendered HTML</li>
    <li>The real product sits behind a login the naive crawl never passed</li>
    <li>The skill was a checklist, not an investigator</li></ul></div>
 </div>
</div>

<h2>Our approach</h2>
<div class=card>
 <p>We rebuilt Blueprint as an <b>autonomous, evidence-first reverse-engineering operator</b>.
 It refuses to guess where it can observe, hunts the hidden API surface, and stops for a
 human go-ahead before building.</p>
 <ol class=steps big>
  <li><b>Intake</b> — confirms target, authorization, credentials, and scope up front (asks
    the right questions instead of assuming).</li>
  <li><b>Deep recon</b> — crawls every screen, <b>captures real network traffic</b>
    (XHR/GraphQL/WS), and mines JS bundles + source maps for hidden/undocumented endpoints,
    exposed data, and leaked secrets — a real <b>security-coverage</b> pass.</li>
  <li><b>Plan &amp; estimate</b> — reconstructs the data model from real responses and writes a
    structured blueprint: system design, tech stack, scale prediction, and a defensible
    <b>time / token / $ estimate</b> with a build-or-not verdict.</li>
  <li><b>Human gate</b> — presents the plan and waits for approval before writing any code.</li>
  <li><b>Build &amp; verify</b> — generates the clone (frontend, typed API client, schema, mock
    backend, design system) then self-audits its own coverage.</li>
 </ol>
 <p class=mut style="margin-bottom:0">Every finding is tagged <span class="tag t-good">OBSERVED</span>
 (captured for real) or <span class="tag t-warn">INFERRED</span> (reasoned). It never presents
 a guess as fact.</p>
</div>

<h2>What the honest approach revealed (target: MProfit)</h2>
<div class=card>
 <table>
  <tr><th>Finding</th><th>Evidence</th></tr>
  <tr><td>Public site is a <b>static (Gatsby) marketing site</b> — no runtime backend</td><td><span class="tag t-good">OBSERVED</span> content baked into page-data JSON; only analytics on the wire</td></tr>
  <tr><td>The real product API is <b>behind login</b> — not captured</td><td><span class="tag t-warn">INFERRED</span> until an authorized login capture is run</td></tr>
  <tr><td>Public crawl yields only <b>~15–20%</b> clone-able coverage</td><td>14 public screens; 0 product screens</td></tr>
  <tr><td>A <b>functional</b> clone (broker parsers + tax engine) is <b>~4–8 weeks</b>, not 1</td><td>fails the 1-week kill-switch; a shell is achievable in a week</td></tr>
 </table>
 <p class=mut style="margin:14px 0 6px">Captured evidence (real screens pulled during recon):</p>
 <div class=gallery>
 {cards}
 </div>
</div>

<h2>The one lever that changes everything</h2>
<div class=card>
 <p><b>An authorized login capture.</b> With credentials, recon captures the real
 authenticated API — converting the entire backend from <span class="tag t-warn">INFERRED</span>
 guesswork into an <span class="tag t-good">OBSERVED</span> contract. That single step is the
 difference between a demo shell and a real clone.</p>
</div>

<h2>Recommendation</h2>
<div class=card>
 <ul class=big>
  <li>Scope the 1-week trial to: <b>authorized capture → real API map → frontend shell + mock
   backend → estimate</b>. That fits a week and de-risks the decision.</li>
  <li>A <b>functional</b> End-Profit clone does not fit a week → per the kill-switch, drop to
   one person and pivot to the standalone GrabOn cloning agent — which Blueprint already is.</li>
  <li>Treat broker parsers &amp; the tax engine as <b>bespoke engineering</b>, not cloning.</li>
 </ul>
 <p class=mut style="margin-bottom:0">Delivered: a <code>/blueprint &lt;url&gt;</code> command
 installable in one line across Claude Code, Cursor, and OpenCode; an autonomous, honest
 skill; and this brief.</p>
</div>

<footer>Blueprint — internal cloning initiative. All backend/API claims here are inferred
from a public crawl and become observed only after an authorized login capture. Prepared for
review; not for external distribution.</footer>

</div></body></html>"""

with open("BLUEPRINT-BRIEF.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wrote BLUEPRINT-BRIEF.html ({len(HTML)//1024} KB, self-contained)")
