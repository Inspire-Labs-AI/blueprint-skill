#!/usr/bin/env python3
# Executive brief — self-contained HTML (images embedded, no paths).
import base64, os
SHOTS = "run/blueprint-out/recon/shots"
PICKS = [("pricing.png","Pricing"),("buy.png","Checkout"),("login.png","Authentication wall"),("sign_up.png","Sign-up")]
def img(n):
    p=os.path.join(SHOTS,n)
    return "data:image/png;base64,"+base64.b64encode(open(p,"rb").read()).decode() if os.path.exists(p) else None
gallery="".join(f'<figure><img src="{d}" alt="{c}"><figcaption>{c}</figcaption></figure>' for c,d in [(c,img(n)) for n,c in PICKS] if d)

HTML=r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Blueprint — Executive Brief</title>
<style>
:root{
 --paper:#14130f; --paper2:#1b1a15; --panel:#1f1d17; --line:#332f25; --line2:#433d2e;
 --ink:#ece6d7; --ink2:#c8c1af; --mut:#948c78; --brass:#c9a24a; --brass2:#e0bd66;
 --d1:#6f7d53; --d2:#8f8a49; --d3:#c09a4a; --d4:#bb7440; --d5:#a8493d;
 --serif:"Iowan Old Style","Palatino Linotype","Book Antiqua",Palatino,Georgia,"Times New Roman",serif;
 --sans:-apple-system,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
 --mono:"SFMono-Regular",ui-monospace,Menlo,Consolas,monospace;}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:0 40px}
@media(max-width:640px){.wrap{padding:0 22px}}
.rule{height:1px;background:var(--line)}
.eyebrow{font:600 11.5px/1 var(--sans);letter-spacing:.28em;text-transform:uppercase;color:var(--brass)}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(38px,6.4vw,74px);line-height:1.02;letter-spacing:-.01em}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(25px,3.6vw,38px);line-height:1.12;letter-spacing:-.005em}
h3{font-family:var(--serif);font-weight:600;font-size:19px;letter-spacing:.005em;color:var(--ink)}
p{color:var(--ink2)} .mut{color:var(--mut)}
a{color:var(--brass2);text-decoration:none;border-bottom:1px solid rgba(201,162,74,.32);transition:border-color .15s}
a:hover{border-bottom-color:var(--brass2)}
td a,td b a{color:inherit;border-bottom:1px dotted rgba(201,162,74,.45)}
td a:hover{color:var(--brass2)}

/* COVER */
.cover{min-height:82vh;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden;padding:80px 0 56px}
.cover::before{content:"";position:absolute;inset:0;background:
 radial-gradient(120% 80% at 78% 8%,rgba(201,162,74,.10),transparent 55%),
 radial-gradient(90% 60% at 0% 100%,rgba(201,162,74,.05),transparent 60%);z-index:0}
.cover>*{position:relative;z-index:1}
.cover .meta{margin-top:34px;display:flex;gap:26px;flex-wrap:wrap;color:var(--mut);font-size:13px;letter-spacing:.04em}
.cover .meta b{color:var(--ink2);font-weight:600}
.cover h1{margin:20px 0 18px;max-width:16ch}
.cover .stand{font-family:var(--serif);font-size:clamp(18px,2.3vw,23px);line-height:1.5;color:var(--ink2);max-width:60ch;font-style:italic}
.brassline{width:64px;height:2px;background:linear-gradient(90deg,var(--brass),transparent);margin:0 0 6px}

/* SECTIONS */
section{padding:64px 0;border-top:1px solid var(--line)}
.head{display:flex;gap:20px;align-items:baseline;margin-bottom:26px}
.num{font-family:var(--serif);font-size:15px;color:var(--brass);letter-spacing:.1em;padding-top:6px;min-width:34px}
.head .t{flex:1}
.lead{font-family:var(--serif);font-size:clamp(19px,2.3vw,23px);line-height:1.5;color:var(--ink);max-width:66ch}
.dropcap::first-letter{font-family:var(--serif);float:left;font-size:62px;line-height:.82;padding:6px 12px 0 0;color:var(--brass)}

/* GRID + CARDS */
.grid{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.g2{grid-template-columns:1fr 1fr}.g3{grid-template-columns:repeat(3,1fr)}
@media(max-width:760px){.g2,.g3{grid-template-columns:1fr}}
.cell{background:var(--paper);padding:26px 24px}
.cell h3{margin-bottom:7px} .cell.hi{background:var(--paper2);box-shadow:inset 3px 0 0 var(--brass)}

/* LABELS */
.lab{display:inline-block;font:600 10.5px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;padding:5px 9px;border:1px solid var(--line2);border-radius:2px;color:var(--ink2);white-space:nowrap}
.lab.on{border-color:rgba(201,162,74,.5);color:var(--brass2)}
.lab.off{color:var(--mut);opacity:.7}
.lab.warn{border-color:rgba(187,116,64,.55);color:#d69a67}

/* TABLE */
table{width:100%;border-collapse:collapse;font-size:14.5px}
caption{text-align:left;font:600 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--mut);padding:0 0 12px}
th{font:600 11px/1 var(--sans);letter-spacing:.13em;text-transform:uppercase;color:var(--mut);text-align:left;padding:12px 14px;border-bottom:1px solid var(--line2)}
td{padding:13px 14px;border-bottom:1px solid var(--line);color:var(--ink2);vertical-align:top}
tbody tr:hover td{background:var(--paper2)}
td b,th+td b{color:var(--ink)}

/* DIFFICULTY CHIPS */
.d{display:inline-block;font:700 11px/1 var(--sans);letter-spacing:.02em;color:#14130f;padding:5px 8px;border-radius:2px}
.dd1{background:var(--d1)}.dd2{background:var(--d2)}.dd3{background:var(--d3)}.dd4{background:var(--d4)}.dd5{background:var(--d5)}
.pr{font:600 11px/1 var(--sans);letter-spacing:.08em;color:var(--brass2);border:1px solid var(--line2);padding:5px 8px;border-radius:2px;white-space:nowrap}

/* FLOW */
.flow{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
@media(max-width:760px){.flow{grid-template-columns:1fr}}
.fstep{background:var(--paper);padding:22px 18px}
.fstep .fn{font-family:var(--serif);font-size:26px;color:var(--brass);line-height:1;margin-bottom:12px}
.fstep.gate{background:var(--panel);box-shadow:inset 0 2px 0 var(--brass)}
.fstep h3{font-size:16px;margin-bottom:5px} .fstep p{font-size:13.5px;color:var(--mut);line-height:1.5}

/* QUOTE */
blockquote{font-family:var(--serif);font-size:clamp(22px,3vw,30px);line-height:1.32;color:var(--ink);max-width:24ch;
 padding-left:24px;border-left:2px solid var(--brass);margin:6px 0}
blockquote cite{display:block;font-family:var(--sans);font-size:13px;font-style:normal;letter-spacing:.04em;color:var(--mut);margin-top:16px}

/* CODE */
pre{background:#0f0e0b;border:1px solid var(--line2);border-radius:3px;padding:16px 18px;overflow:auto;font-family:var(--mono);font-size:13px;color:#d6cba6;line-height:1.65}
code{font-family:var(--mono);color:var(--brass2);font-size:.92em}

/* KPI */
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
@media(max-width:640px){.kpi{grid-template-columns:1fr 1fr}}
.kpi .k{background:var(--paper);padding:24px 18px}
.kpi .v{font-family:var(--serif);font-size:26px;color:var(--ink)}
.kpi .l{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-top:8px}

/* GALLERY */
.gal{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}@media(max-width:760px){.gal{grid-template-columns:1fr 1fr}}
figure{border:1px solid var(--line2);border-radius:3px;overflow:hidden;background:var(--paper2)}
figure img{width:100%;display:block;height:158px;object-fit:cover;object-position:top;filter:grayscale(.15) contrast(1.02)}
figcaption{padding:9px 12px;font-size:11.5px;letter-spacing:.06em;color:var(--mut)}

ul{padding-left:20px}li{margin:7px 0;color:var(--ink2)}
.list-lg li{margin:11px 0;font-size:16.5px}
.hl{color:var(--ink);font-weight:600}
footer{padding:40px 0 64px;color:var(--mut);font-size:12.5px;line-height:1.7;border-top:1px solid var(--line)}
.sig{font-family:var(--serif);font-style:italic;color:var(--ink2)}

/* 10x BANNER */
.banner{display:flex;gap:34px;align-items:center;flex-wrap:wrap;margin:0 0 6px;padding:34px 38px;
 background:linear-gradient(100deg,rgba(201,162,74,.13),rgba(201,162,74,.03));
 border:1px solid rgba(201,162,74,.32);border-radius:4px;position:relative;overflow:hidden}
.banner::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--brass)}
.banner .x{font-family:var(--serif);font-weight:600;font-size:clamp(56px,9vw,104px);line-height:.9;
 color:var(--brass2);letter-spacing:-.02em;flex:0 0 auto}
.banner .bt{flex:1;min-width:260px}
.banner .bt h3{font-family:var(--serif);font-size:clamp(20px,2.6vw,27px);color:var(--ink);line-height:1.2;margin-bottom:8px}
.banner .bt p{color:var(--ink2);font-size:15.5px;max-width:56ch}
</style></head><body>

<div class=wrap>
<header class=cover>
 <div class=brassline></div>
 <div class=eyebrow>Cloning Initiative &middot; Confidential Brief</div>
 <h1>Blueprint</h1>
 <p class=stand>An autonomous agent that reverse-engineers any live product from real evidence,
 tells you precisely what it would cost to rebuild, and — on your word — builds it.</p>
 <div class=meta><span><b>Prepared for</b> &nbsp;Founders &amp; Engineering Leadership</span>
  <span><b>Scope</b> &nbsp;Competitive analysis &amp; build estimation</span>
  <span><b>Status</b> &nbsp;Internal review</span></div>
</header>
</div>

<div class=wrap><section>
 <div class=head><div class=num>01</div><div class=t><div class=eyebrow>The decision</div>
  <h2>Should we clone it — and what will it truly cost?</h2></div></div>
 <p class="lead dropcap">Every "let us clone X" opens with two unknowns: how long, and how much. Naive AI
 hides both — it screenshots the public pages and <span class=hl>invents</span> the backend, so the estimate
 it produces cannot be trusted. Blueprint answers both questions from observed evidence, before a single
 engineer is committed.</p>
 <div class=grid g3 style="margin-top:30px">
  <div class=cell><h3>Time</h3><p class=mut>Per-feature difficulty converted to a realistic day-range — not a guess.</p></div>
  <div class=cell><h3>Cost</h3><p class=mut>Model tokens plus infrastructure run-cost, expressed as a defensible dollar range.</p></div>
  <div class=cell><h3>Risk</h3><p class=mut>What is real versus behind a login, with an unambiguous go / no-go.</p></div>
 </div>
 <div class=banner style="margin-top:36px">
  <div class=x>10&times;</div>
  <div class=bt><h3>Give it a login, and the output multiplies</h3>
   <p>With authorized credentials for the target app, Blueprint captures the <b class=hl>real authenticated API,
   data model, and product screens</b> — instead of inferring them. That single input turns a demo shell into a
   genuine clone and roughly <b class=hl>10&times;</b> the usable output. It is the highest-leverage thing you can provide.</p></div>
 </div>
</section>

<section>
 <div class=head><div class=num>02</div><div class=t><div class=eyebrow>How it is used</div>
  <h2>Three modes, one command</h2></div></div>
 <div class=grid g3>
  <div class=cell><h3>Plan &nbsp;<span class="lab on">default</span></h3><p class=mut>Reconnaissance and a full build blueprint with estimate. Stops at the gate. <i>How hard is this?</i></p></div>
  <div class=cell><h3>Research</h3><p class=mut>Deep investigation into a written dossier — architecture, API surface, competitive read. No build. <i>Study this product.</i></p></div>
  <div class=cell hi><h3>Clone</h3><p class=mut>The full run. It still writes the plan first and presents it, then builds only on your approval. <i>Clone it.</i></p></div>
 </div>
 <p class=mut style="margin-top:18px">Every mode produces a plan. Only <b>Clone</b> writes code — and only after a human says go.</p>
</section>

<section>
 <div class=head><div class=num>03</div><div class=t><div class=eyebrow>Prior art</div>
  <h2>We surveyed the field and distilled the best of it</h2></div></div>
 <p class=lead>Before building, we inventoried the public tooling — sixteen projects across cloning and
 orchestration — classified each, kept the strong ideas, and discarded the vapor.</p>
 <div style="margin-top:26px">
 <table><caption>Cloning engines</caption>
  <tr><th>Project</th><th>Type</th><th>Contribution</th><th>Verdict</th></tr>
  <tr><td><b><a href="https://github.com/JCodesMore/ai-website-cloner-template" target=_blank rel=noopener>ai-website-cloner-template</a></b></td><td><span class=lab>Skill</span></td><td>Parallel builder agents in worktrees (30k&#9733;)</td><td><span class="lab on">Frontend engine</span></td></tr>
  <tr><td><b><a href="https://github.com/namuh-eng/ralph-to-ralph" target=_blank rel=noopener>Ralph-to-Ralph</a></b></td><td><span class=lab>Code</span></td><td>Autonomous inspect &rarr; build &rarr; QA; 52 features in ~4h</td><td><span class="lab on">Flow model</span></td></tr>
  <tr><td><a href="https://github.com/mikulgohil/Morph" target=_blank rel=noopener>Morph</a></td><td><span class=lab>Code</span></td><td>Design tokens, Lighthouse, accessibility QA</td><td><span class="lab on">QA method</span></td></tr>
  <tr><td><a href="https://www.npmjs.com/package/web-cloner" target=_blank rel=noopener>web-cloner</a> &middot; Perfect-Web-Clone</td><td><span class=lab>Code</span></td><td>Multi-stage, block-based pixel fidelity</td><td><span class="lab on">Fidelity</span></td></tr>
  <tr><td><a href="https://github.com/nottelabs/reverse-api-engineer" target=_blank rel=noopener>reverse-api-engineer</a> &middot; <a href="https://github.com/Integuru-AI/Integuru" target=_blank rel=noopener>Integuru</a></td><td><span class=lab>Code</span></td><td>Captured traffic &rarr; typed API client</td><td><span class="lab on">API capture</span></td></tr>
  <tr><td><a href="https://github.com/dakshjain-1616/screenshot2sql" target=_blank rel=noopener>screenshot2sql</a> &middot; <a href="https://www.npmjs.com/package/@grec0/dba-mcp" target=_blank rel=noopener>dba-mcp</a></td><td><span class=lab>Code/MCP</span></td><td>Schema inference &amp; replication</td><td><span class="lab on">Data model</span></td></tr>
  <tr><td><a href="https://www.npmjs.com/package/@veyralabs/saas-reverse" target=_blank rel=noopener>saas-reverse</a></td><td><span class=lab>Skill</span></td><td>SaaS &rarr; feature map and moat</td><td><span class="lab on">Intel</span></td></tr>
  <tr class=mut><td>Product Genesis</td><td>&mdash;</td><td>Claimed autonomous product manager</td><td><span class="lab off">Did not exist</span></td></tr>
 </table></div>
 <div style="margin-top:34px">
 <table><caption>Orchestration harnesses</caption>
  <tr><th>Project</th><th>Role</th><th>Verdict</th></tr>
  <tr><td><b><a href="https://github.com/awslabs/cli-agent-orchestrator" target=_blank rel=noopener>CAO</a></b> &nbsp;<span class=mut>(AWS Labs)</span></td><td>Multi-CLI supervisor &rarr; specialist</td><td><span class="lab on">Pipeline backbone</span></td></tr>
  <tr><td>claude-codex-collab &middot; cc-orchestrator</td><td>Claude as PM, Codex/Kimi as workers, cross-review</td><td><span class="lab on">Cross-model review</span></td></tr>
  <tr><td>codex-orchestrator &middot; harness-subagent</td><td>Parallel workers; a fresh harness has fresh blind spots</td><td><span class="lab on">Parallel build</span></td></tr>
  <tr><td>coord-mcp-server</td><td>Shared file-claim source of truth</td><td><span class="lab on">Conflict control</span></td></tr>
  <tr><td><a href="https://www.npmjs.com/package/agent-spawnkit" target=_blank rel=noopener>agent-spawnkit</a></td><td>Lightweight MCP handoff (our package)</td><td><span class="lab warn">Windows patch pending</span></td></tr>
 </table></div>
 <blockquote style="margin:38px 0 0">A model reviewing its own work repeats its own blind spots; a differently trained one does not.
 <cite>The principle behind Blueprint's cross-model review</cite></blockquote>
</section>

<section>
 <div class=head><div class=num>04</div><div class=t><div class=eyebrow>What we built</div>
  <h2>One agent for daily use; a fleet for scale</h2></div></div>
 <div class=grid g2>
  <div class=cell hi><h3>The Blueprint skill</h3><p class=mut>A single autonomous operator that runs the entire flow itself, with no infrastructure. Installed in one line into Claude Code, Cursor, and OpenCode. This is what an operator runs day to day.</p></div>
  <div class=cell><h3>The agent fleet</h3><p class=mut>Eight specialists running stages in parallel across models — for cloning many products at once. The path to offering it as a service.</p></div>
 </div>
</section>

<section>
 <div class=head><div class=num>05</div><div class=t><div class=eyebrow>The method</div>
  <h2>Investigate, plan, <span style="color:var(--brass)">then you approve</span>, build, verify</h2></div></div>
 <div class=flow>
  <div class=fstep><div class=fn>I</div><h3>Intake</h3><p>Target, authorization, login, scope. It asks; it does not assume.</p></div>
  <div class=fstep><div class=fn>II</div><h3>Deep recon</h3><p>Every screen and its real API traffic captured; hidden endpoints surfaced.</p></div>
  <div class=fstep><div class=fn>III</div><h3>Plan &amp; ETA</h3><p>System design, difficulty, priority, and the time and cost estimate.</p></div>
  <div class="fstep gate"><div class=fn>IV</div><h3>Your gate</h3><p>It stops. Nothing is built until you say go.</p></div>
  <div class=fstep><div class=fn>V</div><h3>Build &amp; verify</h3><p>Clone, mock backend, design system — then a coverage self-audit.</p></div>
 </div>
 <p class=mut style="margin-top:20px">Every finding is marked <span class="lab on">Observed</span> (captured) or <span class=lab>Inferred</span> (reasoned).
 Security coverage is authorized and passive — surface is mapped and reported, never exploited.</p>
</section>

<section>
 <div class=head><div class=num>06</div><div class=t><div class=eyebrow>Orchestration</div>
  <h2>The right model for each task</h2></div></div>
 <table><caption>Model roster</caption>
  <tr><th>Model</th><th>Strength</th><th>Role</th></tr>
  <tr><td><b>Claude Opus</b></td><td>Architecture, planning, hard logic</td><td>Orchestrator &middot; system design &middot; complex codegen</td></tr>
  <tr><td><b>Claude Sonnet</b></td><td>Fast, high-quality bulk code</td><td>Frontend components &middot; routine API routes</td></tr>
  <tr><td><b>Claude Haiku</b></td><td>Inexpensive mechanical work</td><td>Renames &middot; boilerplate &middot; extraction</td></tr>
  <tr><td><b>Codex</b></td><td>Implementation and review</td><td>Parallel build &middot; cross-review of generated code</td></tr>
  <tr><td><b>Gemini</b></td><td>Visual understanding &amp; image generation</td><td>Design tokens &middot; logo and SVG assets</td></tr>
  <tr><td><b>Kimi</b></td><td>Long-context, cost-efficient</td><td>Bulk feature mapping &middot; large-document analysis</td></tr>
  <tr><td><b>Qwen &middot; DeepSeek</b></td><td>Open-source, cost-efficient</td><td>Bulk build and analysis &middot; second-opinion review</td></tr>
 </table>
 <p class=mut style="margin-top:16px">Model choice per stage is what holds quality high while keeping cost sane — Opus where judgment matters, cheaper models for volume.</p>
</section>

<section>
 <div class=head><div class=num>07</div><div class=t><div class=eyebrow>Estimation</div>
  <h2>A difficulty index and a priority order — not S/M/L/XL</h2></div></div>
 <div class=grid g2>
  <div class=cell><h3>Difficulty index</h3><p style="margin-top:6px">
   <span class="d dd1">D1</span> &nbsp;Trivial — static, marketing page<br><br>
   <span class="d dd2">D2</span> &nbsp;Simple — CRUD screen, standard forms<br><br>
   <span class="d dd3">D3</span> &nbsp;Moderate — stateful dashboards, auth, multi-entity<br><br>
   <span class="d dd4">D4</span> &nbsp;Hard — real-time, complex integrations, multi-tenant<br><br>
   <span class="d dd5">D5</span> &nbsp;Research-grade — domain engines (parsers, tax/finance compute)</p></div>
  <div class=cell><h3>Priority order</h3><p style="margin-top:6px">
   <span class=pr>P1 &middot; Base</span> &nbsp;Foundation — auth, shell, navigation, core data<br><br>
   <span class=pr>P2 &middot; Crucial</span> &nbsp;The moat — the features that <i>are</i> the product<br><br>
   <span class=pr>P3 &middot; Add-on</span> &nbsp;Secondary features<br><br>
   <span class=pr>P4 &middot; Later</span> &nbsp;Nice to have</p>
   <p class=mut style="margin-top:20px">Build order follows priority; each item carries its difficulty, its day-range, and its assigned model.</p></div>
 </div>
 <div style="margin-top:30px">
 <table><caption>Worked example &mdash; MProfit</caption>
  <tr><th>Feature / layer</th><th>Difficulty</th><th>Priority</th><th>Estimate</th></tr>
  <tr><td>Marketing site clone</td><td><span class="d dd1">D1</span></td><td><span class=pr>P4</span></td><td>2&ndash;3 days</td></tr>
  <tr><td>Authentication &amp; accounts</td><td><span class="d dd3">D3</span></td><td><span class=pr>P1</span></td><td>~1 week</td></tr>
  <tr><td>Design system &amp; assets</td><td><span class="d dd2">D2</span></td><td><span class=pr>P1</span></td><td>3&ndash;5 days</td></tr>
  <tr><td>Portfolio dashboard &amp; holdings</td><td><span class="d dd3">D3</span></td><td><span class=pr>P2</span></td><td>1&ndash;2 weeks</td></tr>
  <tr><td>XIRR &amp; allocation analytics</td><td><span class="d dd4">D4</span></td><td><span class=pr>P2</span></td><td>~1 week</td></tr>
  <tr><td>Import engine (700+ broker parsers)</td><td><span class="d dd5">D5</span></td><td><span class=pr>P2</span></td><td>2&ndash;4 weeks</td></tr>
  <tr><td>ITR capital-gains tax engine</td><td><span class="d dd5">D5</span></td><td><span class=pr>P2</span></td><td>2&ndash;3 weeks</td></tr>
  <tr><td>Billing</td><td><span class="d dd3">D3</span></td><td><span class=pr>P3</span></td><td>3&ndash;5 days</td></tr>
 </table></div>
 <p class=mut style="margin-top:16px"><b class=hl>Read-out.</b> D1&ndash;D3 fit a one-week shell. The two D5 engines are the true cost centre —
 they dominate the four-to-eight-week functional estimate, and they are bespoke engineering, not cloning.</p>
</section>

<section>
 <div class=head><div class=num>08</div><div class=t><div class=eyebrow>Compliance gate</div>
  <h2>Cloning a product means inheriting its regulatory surface</h2></div></div>
 <p class=lead>A clone that ignores compliance cannot ship. Blueprint flags every regime the product
 triggers at plan time — as a gate the builder must acknowledge — because encryption, consent,
 audit logging, residency and retention are architecture, not afterthoughts.</p>
 <div style="margin-top:26px">
 <table><caption>Triggered regimes &mdash; MProfit (illustrative)</caption>
  <tr><th>Trigger (observed)</th><th>Regime</th><th>Must build</th><th>Effort</th></tr>
  <tr><td>Personal data of Indian users</td><td><b>DPDP Act 2023</b></td><td>Consent, data-residency, erasure / DSAR, breach notice</td><td><span class="d dd3">D3</span></td></tr>
  <tr><td>Card / subscription payments</td><td><b>PCI-DSS</b></td><td>Tokenize via gateway, never store raw card data, SAQ-A scope</td><td><span class="d dd2">D2</span></td></tr>
  <tr><td>Investment / advisory product (India)</td><td><b>SEBI + KYC/AML</b></td><td>KYC onboarding, audit trails, RIA disclosures &mdash; <i>legal review</i></td><td><span class="d dd4">D4</span></td></tr>
  <tr><td>B2B advisor / client data</td><td><b>SOC 2</b></td><td>Access controls, audit logs, retention policy</td><td><span class="d dd3">D3</span></td></tr>
  <tr><td>Analytics &amp; tracking (observed on site)</td><td><b>Consent / ePrivacy</b></td><td>Cookie-consent banner, opt-out</td><td><span class="d dd1">D1</span></td></tr>
 </table></div>
 <p class=mut style="margin-top:16px">Blueprint surfaces obligations; it does not give legal advice. Anything uncertain is flagged
 <span class=lab>needs legal review</span> and gated to a human before build.</p>
</section>

<section>
 <div class=head><div class=num>09</div><div class=t><div class=eyebrow>Evidence &middot; MProfit</div>
  <h2>The honest run found what the fabricated one concealed</h2></div></div>
 <table>
  <tr><th>Finding</th><th>Status</th></tr>
  <tr><td>Public site is a <b>static marketing site</b> — no runtime backend</td><td><span class="lab on">Observed</span></td></tr>
  <tr><td>The real product API sits <b>behind login</b> — reachable only with credentials</td><td><span class=lab>Inferred until login</span></td></tr>
  <tr><td>Public crawl yields only <b>~15&ndash;20%</b> clone-able coverage</td><td>14 public screens; 0 product screens</td></tr>
 </table>
 <p class=mut style="margin:22px 0 10px;letter-spacing:.04em;text-transform:uppercase;font-size:11.5px">Screens captured during reconnaissance</p>
 <div class=gal>__GALLERY__</div>
 <div class="cell hi" style="border:1px solid var(--line2);border-radius:3px;margin-top:20px">
  <h3>The single lever</h3><p class=mut>An <b class=hl>authorized login capture</b> converts the entire backend from inferred guesswork
  into an observed contract — the difference between a demonstration shell and a genuine clone.</p></div>
</section>

<section>
 <div class=head><div class=num>10</div><div class=t><div class=eyebrow>Distribution</div>
  <h2>Published as a plugin — installed in one line</h2></div></div>
 <div class=grid g2>
  <div class=cell><h3>Claude Code &mdash; live now</h3>
   <pre>/plugin marketplace add Inspire-Labs-AI/blueprint-skill
/plugin install blueprint@blueprint-marketplace</pre>
   <p class=mut>The private GitHub repository is the marketplace; no store submission. Access is gated to the organisation.</p></div>
  <div class=cell><h3>Cursor &amp; OpenCode</h3>
   <pre>npx github:Inspire-Labs-AI/blueprint-skill install</pre>
   <p class=mut>Then simply <code>/blueprint &lt;url&gt;</code> in any of the three tools.</p></div>
 </div>
</section>

<section>
 <div class=head><div class=num>11</div><div class=t><div class=eyebrow>Recommendation</div>
  <h2>Scope the week to de-risk the decision</h2></div></div>
 <ul class=list-lg>
  <li>Run a one-week trial: <span class=hl>authorized capture &rarr; real API map &rarr; a P1 shell with mock backend &rarr; estimate.</span> It fits a week and returns a hard go / no-go.</li>
  <li>A functional clone will not fit a week — the two D5 engines govern the timeline. Per the kill-switch, drop to one person and ship the <span class=hl>standalone cloning agent</span>, which Blueprint already is.</li>
  <li>Treat the broker parsers and the tax engine as bespoke engineering, not cloning.</li>
 </ul>
 <div class=kpi style="margin-top:30px">
  <div class=k><div class=v>1 week</div><div class=l>to a decision-grade shell</div></div>
  <div class=k><div class=v>4&ndash;8 wks</div><div class=l>functional clone</div></div>
  <div class=k><div class=v>3 tools</div><div class=l>one-line install</div></div>
  <div class=k><div class=v>Go / No-go</div><div class=l>against your deadline</div></div>
 </div>
</section>

<footer>
 <p class=sig>Blueprint &mdash; internal cloning initiative.</p>
 <p style="margin-top:8px">Backend and API claims are inferred from a public crawl and become observed only after an authorized login capture.
 Security coverage is authorized and passive — surface is mapped and reported, never exploited. Confidential; for internal review, not external distribution.</p>
</footer>
</div>
</body></html>"""
HTML=HTML.replace("__GALLERY__",gallery)
open("BLUEPRINT-BRIEF.html","w",encoding="utf-8").write(HTML)
print(f"wrote BLUEPRINT-BRIEF.html ({len(HTML)//1024} KB)")
