# Claim boundary (read before relying on a result)

What legion-guard does: it fingerprints the `tools/list` this client actually receives (`name`, `description`,
`inputSchema`, JCS RFC 8785 + SHA-256) and compares it with references: your lockfile, the first list seen on this
machine, and, optionally, the latest list signed by the LEGION transparency log (record signature + RFC 9162 inclusion
proof + signed head, keys from a pinned root key).

1. **Warn by default.** Default mode is `warn`: the change is logged and reported; no tool is hidden, no call is refused.
2. **Blocking is opt-in.** Only `mode="block"` hides tools from `list_tools()` and refuses them in `call_tool()`, and
   only the tools for which a source has evidence of a change (changed or new tool).
3. **Fail-open.** A source that is unreachable or whose proof does not verify is reported `UNAVAILABLE` and never blocks,
   in any mode. Internal errors of the guard are logged, never raised to the agent.
4. **UNKNOWN is not a verdict.** LEGION observes only part of the MCP servers. A server absent from the log is `UNKNOWN`:
   that says nothing about the server, good or bad. `UNVERIFIED` means no source could compare anything.
5. **A change is not an attack.** A difference means the list differs from the reference; servers change for legitimate
   reasons. legion-guard does not certify that a server is safe and says nothing about what its tools do.
6. **No legal presumption.** Signed records and inclusion proofs are technical evidence that the log contains a record.
   They are not a qualified timestamp (eIDAS) or any legally recognised proof; the observation time is what the log
   declares.
7. **Single-operator log.** The LEGION log is run by one operator (LEGION). The only witness cosigning its checkpoints
   today is also run by LEGION; there is no independent witness. The log could, in principle, show different histories
   to different clients, and nothing outside LEGION would detect it yet. `LegionSource(witnesses=[...], min_witnesses=N)`
   only adds value with witnesses **you** trust.
8. **First-use pinning trusts the first list it sees.** If that first list was already malicious, it becomes the reference.
9. **Scope of testing.** Tested with the official MCP Python SDK `ClientSession` (streamable HTTP and stdio). Other
   clients and frameworks are not tested.
