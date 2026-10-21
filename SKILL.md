---
name: legion-guard
description: Checks the tool list an MCP server actually sends to this client, before connecting and again during the session, against your approved list, the first list seen, and optionally the list signed by the LEGION transparency log. Use it before connecting an agent to an MCP server, when a server's tools may have changed, or when a tools/list_changed notification arrives mid-session.
allowed-tools: Bash, Read
license: MIT
---

# legion-guard: verify the MCP tools before (and while) using them

Compares the `tools/list` **this client receives** with references (a server can change tool descriptions, even
mid-session) and reports differences. It never calls a tool. Requires `pip install "mcp>=1.24" "cryptography>=50"`; legion-guard 0.2.3 code is bundled (`references/PROVENANCE.md`).

## Claim boundary (always applies; read `references/claim-boundary.md`, tell the user the points that apply)

Warn by default; blocking is opt-in and only for tools a source has evidence changed; fail-open (`UNAVAILABLE` never
blocks); **UNKNOWN is not a verdict**; **a change is not an attack** and nothing certifies a server safe; no legal
presumption (not an eIDAS timestamp); single-operator log with no independent witness yet; first-use pinning trusts the
first list; tested with the official MCP Python SDK only. Network calls and files written: `references/network-and-files.md`.

## 1. Before connecting

```sh
scripts/check_mcp_server.sh <MCP_URL> <SERVER_ID> [--no-legion]   # SERVER_ID = registry id; --no-legion: no LEGION call
```

Sends `initialize` + `tools/list` only. Exit 0 no difference, 1 difference, 2 connection error.
- `DIFFERS_FROM_APPROVED` / `DIFFERS_FROM_SIGNED`: stop; first show the user `differing_tools` / `CHANGED` / `NEW`.
- `NO_APPROVAL`: show tool names and descriptions; only after the user reviewed them, run
  `scripts/approve_mcp_server.sh <MCP_URL> <SERVER_ID> [--lock .mcp-tools.lock.json]`.
- `UNKNOWN` / `UNVERIFIED`: say so plainly; neither a clean bill nor an alarm.

## 2. During the session

```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
import legion_guard
session = legion_guard.wrap(session, "<SERVER_ID>")   # after initialize(); mode="warn" by default
await session.list_tools()   # first call = session reference; later calls are compared with it
print(session.report["verdict"], session.report.get("mid_session_changed_tools"))
```

Re-read on `notifications/tools/list_changed`, before calls that can read files, send data or spend money, and every
few calls. Only the first page of a paginated list is compared. Without client code (no tool called):
`scripts/watch_session.py <MCP_URL> [<SERVER_ID>] --relist 5 --interval 30 [--mode warn|block] [--no-legion]`
(exit 0 no change, 1 change, 2 connection error, 3 nothing verified). Offline self-test: `scripts/selftest.sh` (expects 7/7).

## 3. Reporting

Give the verdict, the tools and the source that saw the difference (`first-use`, `pinned`, `legion`), then the
claim-boundary points that apply. Never call a server "safe", "verified secure" or "certified", nor a log record legal proof. Fields: `references/verdicts.md`.
Library API and custom sources: https://pypi.org/project/legion-guard/0.2.3/.

## 4. Integrity of this package

`references/INTEGRITY.md`: fingerprint of the covered files, its notary log entry, how to check your copy. It proves the
covered files are unchanged since recorded, not that the skill is safe. **Coverage is not total:** the proof files and
`.well-known/` are excluded, so a rewritten `INTEGRITY.md` can state another fingerprint; compare fingerprint and leaf
with those published outside the archive and use a log key you fetched yourself. All code and SKILL.md are covered.
