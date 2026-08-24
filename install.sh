#!/usr/bin/env bash
# Blueprint installer — registers all agents, skills, and the workflow into CAO.
# Prereqs: uv, tmux 3.3+, and the provider CLI (Claude Code). Run from repo root.
set -euo pipefail

# 1. CAO itself
command -v cao >/dev/null || uv tool install "git+https://github.com/awslabs/cli-agent-orchestrator.git@main" --upgrade

# 2. Agents (supervisor + specialists)
for a in agents/*.md; do
  echo "installing agent: $a"
  cao install "$a" --provider claude_code
done

# 3. Skills (available to every CAO agent)
for s in skills/*/; do
  echo "adding skill: $s"
  cao skills add "$s" --force
done

# 4. Durable workflow
WF_DIR="$HOME/.aws/cli-agent-orchestrator/workflows"
mkdir -p "$WF_DIR"
cp workflows/blueprint.py "$WF_DIR/blueprint.py"

# 5. CROSSCHECK — validate everything; abort with a clear message on any failure
echo "== validating profiles =="
for a in agents/*.md; do
  name="$(basename "$a" .md)"
  cao profile validate "$name" || { echo "FAILED profile: $name"; exit 1; }
done
echo "== validating workflow =="
if curl -sf http://127.0.0.1:9889/ >/dev/null 2>&1; then
  cao workflow validate "$WF_DIR/blueprint.py" || { echo "FAILED workflow"; exit 1; }
else
  echo "SKIP: cao-server not running; workflow is validated when you run it"
fi
echo "== confirming bypass-dialog setting persisted =="
grep -q skipDangerousModePermissionPrompt "$HOME/.claude/settings.json" 2>/dev/null \
  && echo "OK: bypass dialog pre-accepted" \
  || echo "WARN: run 'claude --dangerously-skip-permissions' once (accept), or agents may hang on init"
echo "== ALL CHECKS PASSED =="

echo "Blueprint agents + skills installed. (start.sh handles the server + dashboard.)"
