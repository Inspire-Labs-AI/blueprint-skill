---
name: bp-recon
description: Stage 0 capture. Drives a headless browser to grab screenshots, HAR network traffic, DOM, and routes from a target product into blueprint-out/recon/.
---
# bp-recon — capture the target

Goal: everything downstream stages need, pulled once. Uses Playwright (bundled
Chromium). Only capture authenticated/HAR traffic when `target.auth.authorized`.

## Setup (once)
```bash
npm i -g playwright && npx playwright install chromium
```

## Run
Use the helper `recon.mjs` in this skill folder (Playwright script). It:
- visits `target.url` and every discovered same-origin route,
- screenshots each full page to `blueprint-out/recon/shots/<route>.png`,
- records a HAR to `blueprint-out/recon/traffic.har` (skipped if not authorized),
- dumps rendered DOM per route to `blueprint-out/recon/dom/<route>.html`,
- writes the route list.

```bash
node recon.mjs --url "$TARGET_URL" --out blueprint-out/recon \
  ${AUTHORIZED:+--har} ${LOGIN_URL:+--login "$LOGIN_URL"}
```

For authorized targets that need login, capture traffic while logged in so the HAR
contains real API calls — that is what makes Stage 3 `observed` instead of `inferred`.

## Write to manifest
Set `recon.screenshots` (array), `recon.har`, `recon.dom` (dir), `recon.routes`,
and `status.recon = "done"`.

> ponytail: single-pass crawl, same-origin only. Add depth-limit / sitemap parsing
> if the target hides routes behind interaction.
