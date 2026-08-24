# Blueprint runtime: Linux so CAO (tmux) works, with Claude Code + the cloning tools.
FROM node:20-bookworm

# System deps: tmux (CAO), python+pip (screenshot2sql/Integuru), git, uv, poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
      tmux git python3 python3-pip python3-venv pipx curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Claude Code CLI + CAO
RUN npm i -g @anthropic-ai/claude-code
RUN uv tool install "git+https://github.com/awslabs/cli-agent-orchestrator.git@main"

# Playwright + Chromium for recon
RUN npm i -g playwright && npx playwright install --with-deps chromium

WORKDIR /work
# Project is bind-mounted at run time (see docker-compose.yml), so no COPY.
CMD ["bash"]
