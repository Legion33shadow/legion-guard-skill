#!/usr/bin/env python3
"""legion-skill-manifest/v1 : empreinte de couverture non ambiguë d'une skill déballée (sans git, sans réseau).
Construit un manifeste canonique liant type+mode+sha256+chemin de chaque fichier couvert et refuse toute ambiguïté.

  skill_manifest.py ROOT [--print]            # imprime le manifeste et l'empreinte (sha256 du manifeste)
Exclusions par CHEMIN EXACT (jamais un glob) ci-dessous. Exit 0 = manifeste produit ; 2 = ambiguïté/type non prévu (REFUS)."""
import hashlib, os, sys, unicodedata

HEADER = "legion-skill-manifest/v1"
EXACT_EXCLUDES = ["references/INTEGRITY.md", "references/INTEGRITY.bundle.json", ".well-known/mcprush.com-claim.txt"]


def die(m):
    sys.stderr.write("REFUS : %s\n" % m); sys.exit(2)


def check(path):
    if not path or path != path.strip():
        die("chemin vide ou à espaces de bord : %r" % path)
    if any(ord(c) < 0x20 or ord(c) == 0x7f for c in path) or "\\" in path:
        die("caractère de contrôle ou antislash : %r" % path)
    if any(c in ("", ".", "..") for c in path.split("/")):
        die("composant ./../vide : %r" % path)
    if unicodedata.normalize("NFC", path) != path:
        die("chemin non normalisé NFC : %r" % path)


def main():
    root = os.path.abspath(sys.argv[1]); excl = set(EXACT_EXCLUDES)
    files, seen = {}, {}
    for d, dirs, fs in os.walk(root, followlinks=False):
        if ".git" in dirs:
            dirs.remove(".git")
        for n in dirs:
            full = os.path.join(d, n)
            if os.path.islink(full):
                die("lien symbolique (répertoire) : %s" % os.path.relpath(full, root))
        for n in fs:
            full = os.path.join(d, n); rel = os.path.relpath(full, root)
            if os.path.islink(full):
                die("lien symbolique : %s" % rel)
            if not os.path.isfile(full):
                die("type non prévu : %s" % rel)
            check(rel)
            seen.setdefault(rel.lower(), []).append(rel)
            files[rel] = full
    coll = {k: v for k, v in seen.items() if len(v) > 1}
    if coll:
        die("collision de casse : %s" % coll)
    rows = []
    for rel in sorted(files):
        if rel in excl:
            continue
        with open(files[rel], "rb") as f:
            data = f.read()
        mode = "100755" if os.access(files[rel], os.X_OK) else "100644"
        typ = "exec" if mode == "100755" else "file"
        rows.append("%s\t%s\t%s\t%s" % (typ, mode, hashlib.sha256(data).hexdigest(), rel))
    text = HEADER + "\n" + "exact_excludes " + " ".join(sorted(excl)) + "\n" + "".join(r + "\n" for r in rows)
    if "--print" in sys.argv:
        sys.stdout.write(text)
    print("fingerprint", hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
