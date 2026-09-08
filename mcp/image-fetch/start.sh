#!/bin/zsh
set -euo pipefail

cd /AI/infra/mcp/image-fetch
exec /opt/homebrew/bin/uv run -p 3.11 python server.py
