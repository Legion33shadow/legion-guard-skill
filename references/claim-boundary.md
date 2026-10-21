# Claim boundary (read before relying on a result)

legion-guard fingerprints the received `tools/list` (`name`, `description`, `inputSchema`; JCS RFC 8785 + SHA-256) and
compares it with your lockfile, the first list seen here and, optionally, the latest list signed by the LEGION log.

1. **Warn by default.** Mode `warn`: the change is logged and reported; no tool is hidden, no call refused.
2. **Blocking is opt-in.** Only `mode="block"` hides tools from `list_tools()` and refuses them in `call_tool()`, and
   only tools for which a source has evidence of a change (changed or new).
3. **Fail-open.** An unreachable source or a proof that does not verify is `UNAVAILABLE` and never blocks, in any mode.
   Guard errors are logged, never raised to the agent.
4. **UNKNOWN is not a verdict.** LEGION observes only part of the MCP servers; absence from the log says nothing about
   the server, good or bad. `UNVERIFIED` means no source could compare anything.
5. **A change is not an attack.** Servers change for legitimate reasons. legion-guard does not certify that a server is
   safe and says nothing about what its tools do.
6. **No legal presumption.** Signed records and inclusion proofs are technical evidence that the log contains a record,
   not a qualified (eIDAS) timestamp or legally recognised proof; the observation time is what the log declares.
7. **Single-operator log.** LEGION runs the log, and the only witness cosigning its checkpoints today is also LEGION's:
   no independent witness. The log could show different histories to different clients and nothing outside LEGION
   would detect it yet. `LegionSource(witnesses=[...], min_witnesses=N)` only helps with witnesses **you** trust, and
   is `UNAVAILABLE` until they cosigned the current checkpoint (LEGION's witness cosigns hourly: up to about one hour
   per new head, measured 2026-10-18).
8. **First-use pinning trusts the first list it sees.** A malicious first list becomes the reference.
9. **Scope of testing.** Tested with the official MCP Python SDK `ClientSession` (streamable HTTP and stdio) only.
