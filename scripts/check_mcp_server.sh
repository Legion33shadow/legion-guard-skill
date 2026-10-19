#!/usr/bin/env sh
# Pre-connect check: initialize + tools/list on the MCP server (no tools/call), then compare with your lockfile and,
# unless --no-legion is given, with the latest list signed by the LEGION log (network: tlog.legion-api.com).
# Usage: check_mcp_server.sh URL SERVER_ID [--lock FILE] [--no-legion]
# Exit: 0 no difference found, 1 difference found, 2 connection error.
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHONPATH="$HERE${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m legion_guard check "$@"
