#!/usr/bin/env node
// bp-recon capture: the forensic baseline every downstream stage reasons over.
// Saves screenshots + HAR + DOM + JS bundles + response headers + client storage
// + id/pagination samples. See SKILL.md — the agent still has to go EXERCISE the
// features by hand; this script only collects what a mechanical pass can.
//
// Usage: node recon.mjs --url <url> --out <dir> [--har] [--login <url>] [--max 40] [--headed]
//
// ponytail: same-origin BFS, one level of in-page links. Enough for most SaaS
// dashboards; the agent raises --max or drives a browser MCP when a target hides
// routes behind interaction.
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).reduce((a, v, i, arr) => {
    if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1]?.startsWith('--') || arr[i + 1] === undefined ? true : arr[i + 1]]);
    return a;
  }, [])
);

const startUrl = args.url;
const out = args.out || 'blueprint-out/recon';
const MAX = Number(args.max) || 40;
if (!startUrl) { console.error('missing --url'); process.exit(1); }

const origin = new URL(startUrl).origin;
const slug = (u) => (new URL(u).pathname.replace(/\W+/g, '_') || 'root').replace(/^_|_$/g, '') || 'root';

for (const d of ['shots', 'dom', 'bundles', 'storage', 'samples/responses'])
  await mkdir(path.join(out, d), { recursive: true });

// Anything matching these never reaches disk — see SKILL.md "no secrets on disk".
const SECRET_HEADERS = /^(authorization|cookie|set-cookie|x-api-key|x-auth-token|proxy-authorization)$/i;
const scrubHeaders = (h) => Object.fromEntries(
  Object.entries(h).map(([k, v]) => [k, SECRET_HEADERS.test(k) ? `<scrubbed len=${String(v).length}>` : v])
);

const browser = await chromium.launch({ headless: !args.headed });
const context = await browser.newContext(
  args.har ? { recordHar: { path: path.join(out, 'traffic.har'), content: 'embed' } } : {}
);
const page = await context.newPage();

// --- passive collectors: run for the whole session ---------------------------
const headers = [];         // response headers per request — cloud/CDN/server fingerprints
const apiSamples = [];      // JSON response bodies — the raw material for api + datastore
const bundleUrls = new Set();
const consoleLines = [];

page.on('console', (m) => consoleLines.push(`[${m.type()}] ${m.text()}`));

page.on('response', async (res) => {
  const url = res.url();
  if (!url.startsWith(origin) && !/\/api\/|\/graphql|\/v\d\//.test(url)) return;
  try {
    const h = res.headers();
    headers.push({ url, status: res.status(), method: res.request().method(), headers: scrubHeaders(h) });

    const ct = h['content-type'] || '';
    if (/javascript/.test(ct) || /\.js(\?|$)/.test(url)) { bundleUrls.add(url); return; }
    if (!/json/.test(ct)) return;

    const body = await res.text();
    if (body.length > 512_000) return;           // skip absurd payloads
    apiSamples.push({ url, method: res.request().method(), status: res.status(), body });
  } catch { /* body already consumed or navigation raced — not fatal */ }
});

// --- crawl -------------------------------------------------------------------
await page.goto(startUrl, { waitUntil: 'networkidle' }).catch(() => {});

if (args.login && typeof args.login === 'string') {
  console.log('login url given — pausing for manual auth. Log in, then the crawl continues.');
  await page.goto(args.login, { waitUntil: 'networkidle' }).catch(() => {});
  if (args.headed) await page.waitForTimeout(60_000);   // human logs in
  else console.warn('WARN: --login without --headed cannot complete an interactive login.');
}

const links = await page.$$eval('a[href]', (as) => as.map((a) => a.href)).catch(() => []);
const routes = [...new Set([startUrl, ...links])]
  .filter((u) => { try { return new URL(u).origin === origin; } catch { return false; } })
  .slice(0, MAX);
const truncated = links.length > 0 && routes.length >= MAX;

const captured = [];
for (const url of routes) {
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30_000 });
    const name = slug(url);
    const shot = path.join(out, 'shots', `${name}.png`);
    const domFile = path.join(out, 'dom', `${name}.html`);
    await page.screenshot({ path: shot, fullPage: true });
    await writeFile(domFile, await page.content());

    // client storage — feature flags, cached entities, tenancy hints live here
    const storage = await page.evaluate(() => ({
      local: Object.fromEntries(Object.entries(localStorage)),
      session: Object.fromEntries(Object.entries(sessionStorage)),
      cookieNames: document.cookie.split(';').map((c) => c.split('=')[0].trim()).filter(Boolean),
    })).catch(() => null);
    if (storage) await writeFile(path.join(out, 'storage', `${name}.json`), JSON.stringify(storage, null, 2));

    captured.push({ url, status: 'reached', shot, dom: domFile });
    console.log('captured', url);
  } catch (e) {
    captured.push({ url, status: 'blocked', error: e.message });
    console.error('skip', url, e.message);
  }
}

// --- fetch the bundles: the product's source with the names removed ----------
for (const url of bundleUrls) {
  try {
    const res = await page.request.get(url);
    const name = url.split('/').pop().split('?')[0] || 'bundle.js';
    await writeFile(path.join(out, 'bundles', name), await res.text());
    // source maps are pure profit when present — they carry the original file tree
    const map = await page.request.get(url + '.map').catch(() => null);
    if (map && map.ok()) await writeFile(path.join(out, 'bundles', name + '.map'), await map.text());
  } catch { /* bundle vanished or is cross-origin — skip */ }
}

// --- write the samples the datastore stage reasons over ----------------------
for (const [i, s] of apiSamples.entries()) {
  const name = `${String(i).padStart(4, '0')}_${s.method}_${slug(s.url)}.json`;
  await writeFile(path.join(out, 'samples/responses', name), s.body);
}
await writeFile(path.join(out, 'headers.json'), JSON.stringify(headers, null, 2));
await writeFile(path.join(out, 'console.log'), consoleLines.join('\n'));

await context.close();  // flushes HAR
await browser.close();

const summary = {
  target: startUrl,
  routes: captured,
  counts: {
    reached: captured.filter((c) => c.status === 'reached').length,
    blocked: captured.filter((c) => c.status === 'blocked').length,
    bundles: bundleUrls.size,
    json_responses: apiSamples.length,
  },
  truncated_at_max: truncated,
  har: args.har ? path.join(out, 'traffic.har') : null,
  authenticated: Boolean(args.login),
};
await writeFile(path.join(out, 'recon.json'), JSON.stringify(summary, null, 2));

console.log(`\n${summary.counts.reached} routes · ${summary.counts.bundles} bundles · ${summary.counts.json_responses} JSON responses -> ${out}/recon.json`);
if (truncated) console.warn(`WARN: hit --max ${MAX}; more routes exist. Raise --max and note it in coverage.md.`);
if (!args.har) console.warn('NOTE: no --har. Stage 3 (api) will be inference-only, not OBSERVED.');
if (summary.counts.json_responses === 0) console.warn('WARN: 0 JSON responses seen. Either this is a static site, or the app lives on another subdomain — check for app./my./dashboard.');

// self-check: fail loudly if we captured nothing (bad url / blocked / no browser)
if (summary.counts.reached === 0) { console.error('ERROR: 0 routes captured'); process.exit(2); }
