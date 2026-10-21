# Integrity of this package

**Fingerprint (canonical, legion-skill-manifest/v1):** `9931e0c6049a22878b68390b4b78de8605f65faa19f477a870445e5830db2804`
**Notary log:** https://notary.legion-api.com, origin `notary.legion-api.com/proto-v0`, **leaf 8**, received 2026-10-21 06:43:44 UTC (time as declared by the log).
**Log key (pin it):** `legion-notary-proto+9a111253+AeTCvM2cYg1CEzCL3qNbb7IXUdNnllPR3ktBmHroOLKT`
**Rule (legion-skill-manifest/v1):** a canonical manifest, one line per covered file `type⇥mode⇥sha256(content)⇥path`;
the fingerprint is the SHA-256 of that manifest. It binds path, type, mode and content, and **refuses** (does not hash)
symlinks, submodules, unexpected file types and ambiguous paths (control chars, backslash, trailing space, non-NFC,
case collisions). This replaces the earlier `find … | sha256sum` rule (leaves 3–6), which ignored symlinks, file modes
and smuggled `__pycache__`/`references/INTEGRITY*` siblings.
**Excluded, by EXACT path (never a glob):** `references/INTEGRITY.md`, `references/INTEGRITY.bundle.json` (they carry
this proof) and `.well-known/mcprush.com-claim.txt` (marketplace ownership claim). Every other file is covered.
Signed entry, RFC 9162 inclusion proof and C2SP checkpoint: `references/INTEGRITY.bundle.json`.
**Source of truth:** the content of https://github.com/Legion33shadow/legion-guard-skill. Supersedes leaves 3–7 (leaf 7 = the same rule before the `mcp>=1.24` requirement change).

## Check your copy
From the root of your copy (the directory that contains `SKILL.md`), with the key you fetched yourself
(`curl -s https://notary.legion-api.com/notary/v0/vkey`):

    python3 scripts/skill_manifest.py .                       # prints: fingerprint <hex>
    python3 scripts/integrity/verify_bundle.py references/INTEGRITY.bundle.json --sha256 <fingerprint> --log-vkey '<log key>'

or `scripts/verify_integrity.sh '<log key>'` (does both; exit 0 VALID, 1 INVALID, 2 REFUSED on ambiguous/unexpected content).
For an independent check use a verifier you obtained separately, e.g. Go `golang.org/x/mod/sumdb/note` + `sumdb/tlog`.

## What this proves
The exact content recorded (manifest SHA-256 of the covered files, with their type and mode) was entered in an
append-only log with a signed root, verifiable offline. Any change to any covered file — content, path, mode, type —
gives a different fingerprint; a symlink/submodule/ambiguous path makes verification REFUSE rather than silently pass.

## What this does not prove
- Not a safety, security or quality rating of the skill.
- UNKNOWN is not a verdict.
- No legal presumption: not a qualified (eIDAS) timestamp; 'received' is what the log declares.
- Single-operator log, no external witness today (request pending).
- **Coverage is not total (self-reference).** This file and `references/INTEGRITY.bundle.json` cannot be inside their
  own hash, and `.well-known/` is excluded. An attacker who rewrites your copy of THIS file could change the stated
  fingerprint, key or command without changing the fingerprint. Defence: compare the fingerprint and leaf number with
  the ones published **outside** the archive (repo release + marketplace listing), and verify with a key you fetched
  yourself — never one copied from the archive. All code and SKILL.md are covered; only these named proof files are not.
- Checking requires the archive itself.

Prototype. The notary is itself in a test and can be withdrawn.
