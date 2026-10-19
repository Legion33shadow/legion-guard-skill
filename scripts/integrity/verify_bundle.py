#!/usr/bin/env python3
"""Vérifieur autonome d'un bundle legion-notary/v0. N'importe AUCUN code LEGION (stdlib + cryptography).
La clé du journal est fournie hors bande (--log-vkey) : le vkey contenu dans le bundle n'est jamais cru.

  verify_bundle.py BUNDLE.json (--file F | --sha256 HEX) --log-vkey VKEY [--witness-vkey VKEY ...] [--min-witnesses K]
exit 0 = valide ; 1 = invalide (raison imprimée)."""
import argparse, base64, hashlib, json, struct, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def parse_vkey(v):
    name, kid, b64 = v.split("+", 2)
    raw = base64.b64decode(b64)
    if hashlib.sha256(name.encode() + b"\n" + raw).digest()[:4] != bytes.fromhex(kid):
        raise ValueError("vkey : key ID incohérent")
    return name, bytes.fromhex(kid), raw[0], raw[1:]


def node(a, b):
    return hashlib.sha256(b"\x01" + a + b).digest()


def verify_inclusion(leaf, index, size, path, root):          # RFC 9162 §2.1.3.2
    if not 0 <= index < size:
        return False
    fn, sn, r = index, size - 1, leaf
    for p in path:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            r = node(p, r)
            while not fn & 1 and fn != 0:
                fn >>= 1; sn >>= 1
        else:
            r = node(r, p)
        fn >>= 1; sn >>= 1
    return sn == 0 and r == root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle"); g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file"); g.add_argument("--sha256")
    ap.add_argument("--log-vkey", required=True); ap.add_argument("--witness-vkey", action="append", default=[])
    ap.add_argument("--min-witnesses", type=int, default=0)
    a = ap.parse_args()
    b = json.load(open(a.bundle))
    want = (hashlib.sha256(open(a.file, "rb").read()).hexdigest() if a.file else a.sha256.lower())
    entry = base64.b64decode(b["entry_b64"])
    lines = entry.decode().split("\n")
    def fail(m):
        print("INVALIDE :", m); sys.exit(1)
    if len(lines) != 4 or lines[0] != "legion-notary/v0" or lines[3] != "" or not lines[1].startswith("sha256 ") or not lines[2].startswith("received "):
        fail("entrée non canonique")
    if lines[1][7:] != want:
        fail("le SHA-256 de l'entrée (%s) n'est pas celui du fichier/hash fourni (%s)" % (lines[1][7:], want))
    received = int(lines[2][9:])
    # checkpoint (note signée C2SP)
    note = b["checkpoint"]
    if not note.endswith("\n") or "\r" in note:
        fail("note signée malformée (doit finir par une fin de ligne, sans CR — c2sp.org/signed-note)")
    body, sigs = note.split("\n\n", 1); body += "\n"
    origin, size, root_b64 = body.split("\n")[:3]
    if int(size) != b["tree_size"]:
        fail("taille du checkpoint ≠ tree_size du bundle")
    root = base64.b64decode(root_b64, validate=True)
    lname, lkid, lalg, lpub = parse_vkey(a.log_vkey)
    ok_log = False; cosigned = {}
    wk = [parse_vkey(v) for v in a.witness_vkey]
    for l in [x for x in sigs.split("\n") if x]:
        if not l.startswith("— "):
            fail("ligne de signature malformée")
        name, sb64 = l[2:].rsplit(" ", 1); s = base64.b64decode(sb64)
        if name == lname and lalg == 1 and s[:4] == lkid and len(s) == 68:
            try:
                Ed25519PublicKey.from_public_bytes(lpub).verify(s[4:], body.encode()); ok_log = True
            except Exception:
                fail("signature du journal invalide")
        for wname, wkid, walg, wpub in wk:
            if name == wname and walg == 4 and s[:4] == wkid and len(s) == 76:
                ts = struct.unpack(">Q", s[4:12])[0]
                try:
                    Ed25519PublicKey.from_public_bytes(wpub).verify(s[12:], ("cosignature/v1\ntime %d\n" % ts).encode() + body.encode())
                    cosigned[wname] = ts
                except Exception:
                    fail("cosignature de %s invalide" % wname)
    if not ok_log:
        fail("aucune signature valide de la clé de journal attendue")
    leaf = hashlib.sha256(b"\x00" + entry).digest()
    path = [base64.b64decode(x) for x in b["inclusion_proof_b64"]]
    if not all(len(p) == 32 for p in path) or not verify_inclusion(leaf, b["leaf_index"], b["tree_size"], path, root):
        fail("preuve d'inclusion invalide")
    if len(cosigned) < a.min_witnesses:
        fail("%d cosignature(s) valide(s), %d exigée(s)" % (len(cosigned), a.min_witnesses))
    print(json.dumps({"valide": True, "origin": origin, "sha256": want, "leaf_index": b["leaf_index"], "tree_size": b["tree_size"],
                      "received_declare_par_le_journal": received, "temoins": cosigned,
                      "borne_superieure_independante": min(cosigned.values()) if cosigned else None}, ensure_ascii=False))


if __name__ == "__main__":
    main()
