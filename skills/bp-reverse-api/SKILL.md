---
name: bp-reverse-api
description: Stage 3 API. Reuses reverse-api-engineer (HAR->typed client) and Integuru (chained request graphs); falls back to LLM inference from screenshots when no HAR.
---
# bp-reverse-api — reuse

## Get them
```bash
uv tool install reverse-api-engineer            # HAR -> typed client, many langs
git clone https://github.com/Integuru-AI/Integuru vendor/integuru && \
  (cd vendor/integuru && poetry install)        # chained/dynamic request graphs
```

## Live path (authorized + recon.har present)
```bash
reverse-api-engineer agent --url "$TARGET_URL" \
  --prompt "build a typed client for the dashboard API" --json
# chained flows (e.g. add-to-cart -> checkout):
python -m integuru --prompt "reproduce <action>" --har blueprint-out/recon/traffic.har
```
Mark endpoints `confidence:"observed"`, `api.live=true`.

## Inference path (screenshots only)
No HAR? Infer endpoints, request/response shapes, and auth flow from `recon` DOM +
`intel.feature_map`. Emit a stub typed client. Mark `confidence:"inferred"`,
`api.live=false`.

## Write to manifest (`api`)
`endpoints`, `client_path`, `language`, `auth_flow`, `live`; `status.api="done"`.
