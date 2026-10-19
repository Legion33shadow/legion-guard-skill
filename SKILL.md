---
name: legion-guard
description: Checks the tool list an MCP server actually sends to this client, before connecting and again during the session, against your approved list, the first list seen, and optionally the list signed by the LEGION transparency log. Use it before connecting an agent to an MCP server, when a server's tools may have changed, or when a tools/list_changed notification arrives mid-session.
when_to_use: Before the first use of an MCP server in an agent; before calling a sensitive tool on a server approved earlier; when the server sends notifications/tools/list_changed; when the user asks whether an MCP server's tools changed.
allowed-tools: Bash, Read
license: MIT
---

# legion-guard: verify the MCP tools before (and while) using them

An agent reads an MCP server's tool descriptions as instructions. A server can expose other tools, or the same tools
with other descriptions, than the ones approved earlier, and it can change them in the middle of a session. This skill
compares what **this client actually receives** with references, and reports the difference. It never calls a tool.

Requirements (install once): `pip install "mcp>=2.2" "cryptography>=50"`. The legion-guard 0.2.3 code is bundled in
`scripts/legion_guard/` (see `references/PROVENANCE.md`).

## Claim boundary (always applies; tell the user when you report a result)

- **Warn by default.** Changes are reported; nothing is hidden or refused.
- **Blocking is opt-in** (`--mode block` / `mode="block"`), and blocks only tools for which a source has evidence of a change.
- **Fail-open.** An unreachable source or an invalid proof is `UNAVAILABLE` and never blocks; guard errors never break the agent.
- **UNKNOWN is not a verdict.** LEGION observes only part of the servers; absence from the log says nothing about a server.
- **A change is not an attack**, and no result certifies that a server or its tools are safe.
- **No legal presumption.** Signatures and inclusion proofs are technical evidence, not a qualified (eIDAS) timestamp or legal proof.
- **Single-operator log.** The LEGION log has one operator, and its only cosigning witness today is run by LEGION too: there is no independent witness yet.
- First-use pinning trusts the first list it sees. Tested with the official MCP Python SDK only.

Full text: `references/claim-boundary.md`. Network calls and files written: `references/network-and-files.md`.

## 1. Before connecting (pre-connect check)

```sh
scripts/check_mcp_server.sh <MCP_URL> <SERVER_ID>            # SERVER_ID = registry id, e.g. com.dexpaprika/dexpaprika
scripts/check_mcp_server.sh <MCP_URL> <SERVER_ID> --no-legion   # local references only, no LEGION network call
```

It sends `initialize` + `tools/list` only. Read `approval` (your lockfile) and `legion.state` (signed log).
Exit code 0 = no difference found, 1 = difference found, 2 = connection error.

- `DIFFERS_FROM_APPROVED` or `DIFFERS_FROM_SIGNED`: stop and show the user the tools listed in `differing_tools` /
  `CHANGED` / `NEW` before using the server.
- `NO_APPROVAL`: no approved list yet. Show the user the tool names and descriptions; only after the user has reviewed
  them, record the approval:

```sh
scripts/approve_mcp_server.sh <MCP_URL> <SERVER_ID> [--lock .mcp-tools.lock.json]
```

- `UNKNOWN` / `UNVERIFIED`: say so plainly; it is not a clean bill of health and not an alarm.

## 2. During the session (mid-session check)

A server may serve a harmless list first and change a description after a few calls. Inside a Python MCP client,
wrap the session once, then read `tools/list` again at the right moments; each re-read in the same session is compared
with the list seen at the start:

```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
import legion_guard
session = legion_guard.wrap(session, "<SERVER_ID>")           # after session.initialize(); mode="warn" by default
await session.list_tools()                                     # reference for this session
# ... later: on notifications/tools/list_changed, before a sensitive call, or periodically:
await session.list_tools()
print(session.report["verdict"], session.report.get("mid_session_changed_tools"))
```

Re-read `tools/list` when the server sends `notifications/tools/list_changed`, before any tool call that can read
files, send data or spend money, and after every few calls in long sessions. Only the first page of a paginated list
is compared.

Without your own client code, observe one session from the command line (no tool is called):

```sh
scripts/watch_session.py <MCP_URL> [<SERVER_ID>] --relist 5 --interval 30 [--mode warn|block] [--no-legion]
```

Exit code 0 = no change, 1 = change detected, 2 = connection error, 3 = nothing could be verified.

## 3. Check that the bundled code works (offline)

```sh
scripts/selftest.sh     # local fake MCP server changes a description after 3 calls; expects 7/7
```

## 4. How to report to the user

State the verdict, the tools involved and which source saw the difference (`first-use`, `pinned`/lockfile, `legion`),
then the claim-boundary points that apply. Do not call a server "safe", "verified secure" or "certified"; do not present
a log record as legal proof. Field-by-field meanings: `references/verdicts.md`. Library API and sources
(`FirstUseSource`, `PinnedSource`, `LegionSource`, custom sources): `references/legion-guard-README.md`.

## 5. Integrity of this package

The content of this skill (the files covered by the rule given in `references/INTEGRITY.md`) is recorded in a public append-only notary log
with a signed inclusion proof. `references/INTEGRITY.md` gives the fingerprint, the log entry and how to check that
your copy is exactly the recorded one. This proves the covered files are unchanged since they were recorded; it does not
prove that the skill is safe or correct.

**Coverage is not total.** The fingerprint cannot cover its own proof files: `references/INTEGRITY.md` and
`references/INTEGRITY.bundle.json` are excluded by necessity (a file cannot contain its own hash), and so is
`.well-known/` (marketplace ownership claims, not skill content). An attacker who can rewrite your copy of
`references/INTEGRITY.md` could therefore change the stated fingerprint, log key or verification command **without
changing the fingerprint itself**. The only defence is out-of-band: compare the fingerprint and leaf number with the
ones published outside this archive (the repository release and the marketplace listing), and verify with a log key
you obtained yourself (`curl https://notary.legion-api.com/notary/v0/vkey`), never one copied from the archive. Every
covered file — all code, every script, SKILL.md itself — is bound by the fingerprint; only these named proof files are not.
