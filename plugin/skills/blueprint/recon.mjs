#!/usr/bin/env node
// bp-recon capture: screenshots + HAR + DOM + routes for a target product.
// Usage: node recon.mjs --url <url> --out <dir> [--har] [--login <url>]
// ponytail: same-origin BFS, one level of in-page links. Enough for most SaaS
// dashboards; add auth/interaction crawling only if a target hides routes.
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
if (!startUrl) { console.error('missing --url'); process.exit(1); }

const origin = new URL(startUrl).origin;
const slug = (u) => (new URL(u).pathname.replace(/\W+/g, '_') || 'root').replace(/^_|_$/g, '') || 'root';

await mkdir(path.join(out, 'shots'), { recursive: true });
await mkdir(path.join(out, 'dom'), { recursive: true });

const browser = await chromium.launch({ headless: !args.headed });
const context = await browser.newContext(
  args.har ? { recordHar: { path: path.join(out, 'traffic.har'), content: 'embed' } } : {}
);
const page = await context.newPage();

// Discover same-origin routes from the landing page, then visit start + those.
await page.goto(startUrl, { waitUntil: 'networkidle' }).catch(() => {});
const links = await page.$$eval('a[href]', (as) => as.map((a) => a.href));
const routes = [...new Set([startUrl, ...links])].filter((u) => { try { return new URL(u).origin === origin; } catch { return false; } }).slice(0, 40);

const screenshots = [], doms = [];
for (const url of routes) {
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    const shot = path.join(out, 'shots', `${slug(url)}.png`);
    await page.screenshot({ path: shot, fullPage: true });
    const domFile = path.join(out, 'dom', `${slug(url)}.html`);
    await writeFile(domFile, await page.content());
    screenshots.push(shot); doms.push(domFile);
    console.log('captured', url);
  } catch (e) { console.error('skip', url, e.message); }
}

await context.close(); // flushes HAR
await browser.close();

const summary = { routes, screenshots, dom: path.join(out, 'dom'), har: args.har ? path.join(out, 'traffic.har') : null };
await writeFile(path.join(out, 'recon.json'), JSON.stringify(summary, null, 2));
console.log(`\n${screenshots.length} routes captured -> ${out}/recon.json`);

// self-check: fail loudly if we captured nothing (bad url / blocked / no browser)
if (screenshots.length === 0) { console.error('ERROR: 0 screenshots captured'); process.exit(2); }
