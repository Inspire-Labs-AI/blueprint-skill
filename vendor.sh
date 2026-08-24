#!/usr/bin/env bash
# Pull the real cloning tools the bp-* skills wrap. Run from repo root, inside WSL/Linux/mac.
set -euo pipefail
mkdir -p vendor

# Frontend — parallel per-section cloner (Stage 5)
[ -d vendor/cloner-template ] || git clone --depth 1 \
  https://github.com/JCodesMore/ai-website-cloner-template vendor/cloner-template

# Database — screenshot -> schema (Stage 2)
[ -d vendor/screenshot2sql ] || git clone --depth 1 \
  https://github.com/dakshjain-1616/screenshot2sql vendor/screenshot2sql
pip install -r vendor/screenshot2sql/requirements.txt

# API — chained request graphs (Stage 3, live path)
[ -d vendor/integuru ] || git clone --depth 1 \
  https://github.com/Integuru-AI/Integuru vendor/integuru
( cd vendor/integuru && poetry install )

# API — HAR -> typed client (Stage 3, installed as a CLI, not vendored)
command -v reverse-api-engineer >/dev/null || uv tool install reverse-api-engineer

# Intel — saas-reverse is a Claude skill bundle (Stage 1); extract from npm into vendor/
if [ ! -d vendor/saas-reverse ]; then
  npm pack @veyralabs/saas-reverse
  mkdir -p vendor/saas-reverse && tar -xzf veyralabs-saas-reverse-*.tgz -C vendor/saas-reverse --strip-components=1
  rm -f veyralabs-saas-reverse-*.tgz
fi

# Recon browser (Stage 0)
npm i -g playwright && npx playwright install chromium

echo "vendored -> ./vendor/ . Set OPENROUTER_API_KEY for screenshot2sql before running."
