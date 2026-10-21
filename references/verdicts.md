# Reading the results

`check_mcp_server.sh` (exit codes in SKILL.md):
- `approval`: `NO_APPROVAL` | `MATCHES_APPROVED` | `DIFFERS_FROM_APPROVED`; per tool `APPROVED`, `CHANGED`, `NEW`, `NOT_APPROVED`; `removed_since_approval`.
- `legion.state`: `MATCHES_SIGNED` | `DIFFERS_FROM_SIGNED` (+ `differing_tools`) | `UNKNOWN` (not in the log; not a verdict) | `UNVERIFIED` (log unreachable or proof invalid).

`watch_session.py` and `legion_guard.wrap(...)`:
- Per source: `MATCHES` | `DIFFERS` | `PINNED_NOW` (reference just created) | `UNKNOWN` | `UNAVAILABLE`.
- `verdict`: `CHANGE_DETECTED` | `NO_CHANGE_DETECTED` | `UNVERIFIED` (no source could compare) | `GUARD_ERROR` (internal error, nothing blocked).
- `mid_session_changed_tools`: changed **after** the first `tools/list` of the same session. `hidden_tools`: `block` mode only.
