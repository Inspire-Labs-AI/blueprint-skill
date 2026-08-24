#!/usr/bin/env bash
# ONE command to boot Blueprint inside the container.
#   ./start.sh                      -> install + start server + dashboard, then wait for your commands
#   ./start.sh https://example.com  -> ...and immediately kick off a clone of that URL
set -euo pipefail
export IS_SANDBOX=1                       # lets Claude run bypass-permissions as root in-container

echo "== installing/validating agents + skills =="
./install.sh

echo "== starting cao-server (logs -> /tmp/cao.log, no more terminal spam) =="
pkill -f cao-server 2>/dev/null || true; sleep 1
CAO_PROVIDER_INIT_TIMEOUT=180 cao-server --host 0.0.0.0 >/tmp/cao.log 2>&1 &
sleep 4

echo "== starting dashboard (logs -> /tmp/dashboard.log) =="
pkill -f dashboard.py 2>/dev/null || true
python3 dashboard.py >/tmp/dashboard.log 2>&1 &

cat <<EOF

READY.
  Dashboard : open on Windows -> ...\\blueprint\\run\\blueprint-out\\board.html
  Clone now : cao launch "Clone <URL>" --agents blueprint-don --working-directory ./run --auto-approve
  Watch     : cao session list
  Logs      : tail -f /tmp/cao.log
EOF

if [ "${1:-}" ]; then
  echo "== launching clone of $1 =="
  cao launch "Clone $1" --agents blueprint-don --working-directory ./run --auto-approve
fi
