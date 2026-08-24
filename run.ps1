# Blueprint — one command: give a URL, get run/blueprint-out/blueprint.md
# Usage:  .\run.ps1 -Url "https://www.mprofit.in/"  [-Headed]
param(
  [Parameter(Mandatory=$true)][string]$Url,
  [switch]$Headed
)
$ErrorActionPreference = "Stop"
$out = "run/blueprint-out"
New-Item -ItemType Directory -Force -Path "$out/recon" | Out-Null

# Stage 0 — recon (Node + Playwright)
Write-Host "== recon: $Url ==" -ForegroundColor Cyan
$reconArgs = @("skills/bp-recon/recon.mjs", "--url", $Url, "--out", "$out/recon")
if ($Headed) { $reconArgs += "--headed" }
node @reconArgs

# Stages 1-6 — Claude Code headless produces the master blueprint
Write-Host "== synthesis: writing $out/blueprint.md ==" -ForegroundColor Cyan
$prompt = @"
Load the bp-blueprint skill and follow it exactly. Target URL: $Url.
Read every screenshot and DOM file under $out/recon (recon.json lists them),
then write the complete master document to $out/blueprint.md with all 9 sections,
and update $out/manifest.json. Evidence-led: tag every claim observed or inferred.
"@
claude -p $prompt --allowedTools "Read,Write,Glob,Bash"

Write-Host "`nDone -> $out/blueprint.md" -ForegroundColor Green
