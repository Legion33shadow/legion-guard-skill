# Every network call and file write (exhaustive for this skill)

Network calls:
- Always: the MCP server URL **you** pass — `initialize` + `tools/list` (re-lists if you ask); never `tools/call`.
- Only with a SERVER_ID and without `--no-legion`: `https://tlog.legion-api.com/tlog/v1` (override: env `LEGION_LOCK_BASE`
  or `LegionSource(base=...)`) — `GET /servers/{id}/latest`, `GET /keyring`; `GET /checkpoint` only with `min_witnesses>0`.

Nothing else: no telemetry, no analytics, no update check. `selftest.sh` (local stdio fake server), `verify_integrity.sh`
and `integrity/verify_bundle.py` make no network call. `vendor/legion_tlog_verify.py` can fetch
`https://tlog.legion-api.com/tlog/v0` and `https://legion-api.com/passport/legion-ed25519.pub` only from its own command
line, unused here; its `https://legion-api.com/tlog/` (User-Agent) and `http://www.w3.org/2000/svg` are not requests.

Files written: `~/.cache/legion-guard/pins.json` (or `--pins FILE`), first-use pins; `.mcp-tools.lock.json` (or
`--lock FILE`), only by `approve_mcp_server.sh`.

Dependencies: `mcp>=1.24` (first version with `streamable_http_client`;
measured 2026-10-21: 1.23.3 fails; 1.24.0, 1.30.0, 2.1.1, 2.3.0 pass), `cryptography>=50`. GHSA-84m7-p3x7-pcfv (StreamableHTTP sessions,
fixed in 1.30.0 / 2.2.0) is server-side; this skill only uses the client. If you also run MCP servers here, use 1.30.0+ or 2.2.0+.
