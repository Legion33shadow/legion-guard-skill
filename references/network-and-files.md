# Every network call and file write (exhaustive for this skill)

## Network calls made by the scripts of this skill
| When | Destination | Requests |
|---|---|---|
| always | the MCP server URL **you** pass | `initialize` + `tools/list` (repeated if you ask for re-lists). The guard itself never sends `tools/call`. |
| only if a SERVER_ID is given and `--no-legion` is absent | `https://tlog.legion-api.com/tlog/v1` (override: env `LEGION_LOCK_BASE`, or `LegionSource(base=...)`) | `GET /servers/{id}/latest`, `GET /keyring`; `GET /checkpoint` only with `min_witnesses>0` |

Nothing else: no telemetry, no analytics, no update check. Without a SERVER_ID, or with `--no-legion`, the only
network peer is the MCP server itself. `scripts/selftest.sh` makes no network call (it runs a local stdio server).

## URL literals present in the code but NOT reached by this skill
`scripts/legion_guard/vendor/legion_tlog_verify.py` is the standalone LEGION verifier; its own command line (not used by
this skill) can fetch `https://tlog.legion-api.com/tlog/v0` and `https://legion-api.com/passport/legion-ed25519.pub`.
It also contains `https://legion-api.com/tlog/` (User-Agent string) and `http://www.w3.org/2000/svg` (SVG namespace),
which are not requests.

## Files written
| File | When |
|---|---|
| `~/.cache/legion-guard/pins.json` (or `--pins FILE`) | first-use pinning: first list seen per server |
| `.mcp-tools.lock.json` in the current directory (or `--lock FILE`) | only `approve_mcp_server.sh` |

## Dependencies (installed by you)
`pip install "mcp>=2.2" "cryptography>=50"` — `mcp` 2.2.0 or later (versions 2.0.0–2.1.1 and 1.8.0–1.29.1 are affected by
GHSA-84m7-p3x7-pcfv on the server side); `cryptography` 50 or later verifies the Ed25519 signatures (earlier versions have published advisories in OSV).

## Code that can open a connection
- `scripts/legion_guard/__main__.py`, `scripts/watch_session.py`: connect to the MCP server URL you pass (MCP SDK `streamable_http_client`).
- `scripts/legion_guard/_lock.py`, `scripts/legion_guard/sources.py`: requests to the LEGION log listed above (`urllib.request`).
- `scripts/legion_guard/vendor/legion_tlog_verify.py`: only through its own command line, not used by this skill.
- `scripts/verify_integrity.sh`, `scripts/integrity/verify_bundle.py`: no network call (you pass the log key; you may fetch it yourself from `https://notary.legion-api.com/notary/v0/vkey`).
- `scripts/selftest/test_midsession.py`: starts `scripts/selftest/fake_midsession_server.py` as a local subprocess over stdio; no network.
