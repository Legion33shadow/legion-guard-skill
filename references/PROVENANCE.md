# Provenance of the bundled code

The code in `scripts/legion_guard/` is copied byte for byte from the wheel `legion_guard-0.2.3-py3-none-any.whl`
published on PyPI by its author (sha256 `65f491e415f83ddcf8a3d909b2ab83cf9f4a44dca2a6c23b408ded47aa8c20b1`, source: https://github.com/Legion33shadow/legion-guard, commit `6111e8e`).
`LICENSE` is identical to the wheel's license file (MIT).

| File | sha256 | Status |
|---|---|---|
| `scripts/legion_guard/__init__.py` | `8181a2de1690cce0cd8bb86a0d4b3554719c98d561e6b33f75ed247794882a9d` | identical to the wheel |
| `scripts/legion_guard/__main__.py` | `844ecd3c26896d185f1d173372e87a7a32dc6da68e132d340f2f20cb32065314` | identical to the wheel |
| `scripts/legion_guard/_lock.py` | `8a60926324eadfab0793eb317eff9d6c49b72312c107e1c374384fb24e5f49d0` | identical to the wheel |
| `scripts/legion_guard/sources.py` | `59540e41e184e5935665fe03809da8f28c18aef66dde668af52f7a53d0570b49` | identical to the wheel |
| `scripts/legion_guard/vendor/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | identical to the wheel |
| `scripts/legion_guard/vendor/legion_tlog_verify.py` | `1301aa747eb8457dd78eca2997795961a706d2a32a203dd3c3b2105675160325` | identical to the wheel |
| `legion_guard/vendor/legion_verify_mirror.py` | — | **not bundled** (see below) |

**Not bundled:** `legion_guard/vendor/legion_verify_mirror.py`. Its pure-Python Ed25519 fallback follows the reference
code of RFC 8032 section 6, which is not original LEGION code. This skill therefore requires `cryptography`; with it
installed, legion-guard never imports that file.

The wrapper scripts (`check_mcp_server.sh`, `approve_mcp_server.sh`, `watch_session.py`, `selftest.sh`) are written for
this skill. `scripts/selftest/` comes from the legion-guard repository's tests; in `fake_midsession_server.py` the changed description is a neutral test string instead of the repository's simulated injection text.
