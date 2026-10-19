#!/usr/bin/env sh
# Offline self-test of the bundled code: a local fake MCP server (stdio) changes a tool description after 3 calls.
# Checks: warn mode reports the mid-session change without removing anything; block mode hides and refuses the tool.
# No network call; HOME is redirected to a temporary directory. Requires: mcp>=2.2, cryptography>=50.
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$HERE/selftest/test_midsession.py"
