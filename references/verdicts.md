# Reading the results

## `check_mcp_server.sh` (one connection)
- `approval`: `NO_APPROVAL` (no lockfile entry) | `MATCHES_APPROVED` | `DIFFERS_FROM_APPROVED`; per tool: `APPROVED`, `CHANGED`, `NEW`, `NOT_APPROVED`; `removed_since_approval`.
- `legion.state`: `MATCHES_SIGNED` | `DIFFERS_FROM_SIGNED` (+ `differing_tools`) | `UNKNOWN` (not in the log; not a verdict) | `UNVERIFIED` (log unreachable or proof invalid).
- Exit code: 0 no difference found, 1 difference found, 2 connection error.

## `watch_session.py` and `legion_guard.wrap(...)` (inside a session)
- Per source: `MATCHES` | `DIFFERS` | `PINNED_NOW` (first connection, reference just created) | `UNKNOWN` | `UNAVAILABLE`.
- `verdict`: `CHANGE_DETECTED` | `NO_CHANGE_DETECTED` | `UNVERIFIED` (no source could compare) | `GUARD_ERROR` (internal error, nothing blocked).
- `mid_session_changed_tools`: tools whose definition changed **after** the first `tools/list` of the same session.
- `hidden_tools`: only in `block` mode.
- Exit code of `watch_session.py`: 0 no change, 1 change, 2 connection error, 3 UNVERIFIED / GUARD_ERROR.

## What to tell the user
Report the verdict, the tools involved and the source that saw the difference, then the claim boundary points that
apply (at least: a change is not an attack; UNKNOWN is not a verdict). Never describe a result as a security
certification or a legal proof.
