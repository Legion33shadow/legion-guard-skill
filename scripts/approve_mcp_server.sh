#!/usr/bin/env sh
# Writes the tool list received NOW as the approved list in the lockfile (default .mcp-tools.lock.json).
# Run only after a human has reviewed the tools. No network call other than the MCP server itself.
# Usage: approve_mcp_server.sh URL SERVER_ID [--lock FILE]
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHONPATH="$HERE${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m legion_guard approve "$@"
