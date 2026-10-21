# Integrity of this package

**Fingerprint (legion-skill-manifest/v1):** `bdd7520c6ae129fd621085957d8412e440fc14a401c1a91b134de6221cd048bf`
**Notary log:** https://notary.legion-api.com, origin `notary.legion-api.com/proto-v0`, **leaf 10**, received 2026-10-21 16:43:02 UTC (as declared by the log). Supersedes leaves 3–9.
**Log key (pin it):** `legion-notary-proto+9a111253+AeTCvM2cYg1CEzCL3qNbb7IXUdNnllPR3ktBmHroOLKT`
**Rule:** fingerprint = SHA-256 of a manifest with one line `type⇥mode⇥sha256(content)⇥path` per covered file;
symlinks, submodules, unexpected types and ambiguous paths are refused, not hashed. **Excluded by exact path:** `references/INTEGRITY.md`,
`references/INTEGRITY.bundle.json` (they carry this proof), `.well-known/mcprush.com-claim.txt` (marketplace claim).
Signed entry, RFC 9162 inclusion proof, C2SP checkpoint: `references/INTEGRITY.bundle.json`.
Source of truth: https://github.com/Legion33shadow/legion-guard-skill.

**Check your copy** from the directory containing `SKILL.md`, with a key you fetched yourself
(`curl -s https://notary.legion-api.com/notary/v0/vkey`): `scripts/verify_integrity.sh '<log key>'` (exit 0 VALID,
1 INVALID, 2 REFUSED).
Independent check: a verifier obtained separately, e.g. Go `golang.org/x/mod/sumdb/note` + `sumdb/tlog`.

**Proves:** the covered files (content, path, mode, type) are exactly those recorded in an append-only log with a signed
root, verifiable offline. **Does not prove:** safety, security or quality of the skill; UNKNOWN is not a verdict; no legal
presumption (not an eIDAS timestamp; 'received' is what the log declares); single-operator log, no external witness today.
**Coverage is not total:** whoever rewrites your copy of this file can change the stated fingerprint, key or command
without changing the fingerprint. Defence: compare fingerprint and leaf with those published outside the archive
(repository, marketplace listing) and verify with a key you fetched yourself. Checking requires the archive itself.
Prototype: the notary is in a test and can be withdrawn.
